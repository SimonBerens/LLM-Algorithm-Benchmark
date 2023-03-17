import asyncio

import yaml
import json

from execution_pipeline.code_exectuors.python_executor import PythonExecutor
from execution_pipeline.evaluators.stripped_exact_match import StrippedExactMatch
from execution_pipeline.languages import SupportedLanguage
from execution_pipeline.pipelines.default_pipeline import DefaultPipeline
from execution_pipeline.task_runners.default_task_runner import DefaultTaskRunner
from execution_pipeline.types import Executor, TestResult
from paths import *
from utils import force_write_to


class DummyLlmPythonExecutor(Executor):
    @property
    def name(self) -> str:
        return "dummy_llm_python_executor"

    def __init__(self):
        pass

    async def execute(self, code_path: Path, input_paths: list[Path]) -> list[str]:
        return [""] * len(input_paths)


code_executor_mapping = {SupportedLanguage.PYTHON: PythonExecutor()}
llm_executor_mapping = {SupportedLanguage.PYTHON: [DummyLlmPythonExecutor()]}

task_runner = DefaultTaskRunner(code_executor_mapping, llm_executor_mapping, StrippedExactMatch())

print("Running pipeline...")
results: list[TestResult] = asyncio.run(DefaultPipeline(task_runner).run())

tmp_eval_set_yaml = []
algorithmic_thinking_yaml = {}
for result in results:
    task_name = result.path.stem
    tmp_eval_set_yaml.append(f"algorithmic-thinking-{task_name}")
    algorithmic_thinking_yaml.update({
        f"algorithmic-thinking-{task_name}": {
            "id": f"algorithmic-thinking-{task_name}.s1.simple-v0",
            "description": result.metadata[
                               "description"] + " (from https://github.com/SimonBerens/LLM-Algorithm-Benchmark)",
            "metrics": ["accuracy"],

        },
        f"algorithmic-thinking-{task_name}.s1.simple-v0": {
            "class": "evals.elsuite.basic.match:Match",
            "args": {
                "samples_jsonl": f"algorithmic-thinking/{task_name}/samples.jsonl"
            }
        }
    })
    sample_jsonl = []
    for subtest_result in result.subtest_results:
        input_text = subtest_result.input_path.read_text()
        code_str = subtest_result.code_path.read_text()
        code_output = subtest_result.code_output.strip()
        sample_jsonl.append({
            "input": [
                {"role": "system",
                 "content": "You will be given code and input. Predict the output. Respond with the exact output without any extra characters."},
                {"role": "user", "content": f"Input:\n{input_text}\n\nCode:\n{code_str}"},
            ],
            "ideal": code_output,
        })
    force_write_to(eval_samples_path.joinpath(f"algorithmic-thinking/{task_name}/samples.jsonl"), "\n".join(map(json.dumps, sample_jsonl)))
    
force_write_to(evals_path.joinpath("evals/algorithmic-thinking.yaml"), yaml.dump(algorithmic_thinking_yaml))

eval_set_yaml = {
    "algorithmic-thinking": {
        "evals": tmp_eval_set_yaml
    }
}
force_write_to(evals_path.joinpath("eval_sets/algorithmic-thinking.yaml"), yaml.dump(eval_set_yaml))
