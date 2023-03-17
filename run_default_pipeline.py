import asyncio

from langchain import OpenAI, Cohere

import paths
from execution_pipeline.code_exectuors.python_executor import PythonExecutor
from execution_pipeline.evaluators.stripped_exact_match import StrippedExactMatch
from execution_pipeline.languages import SupportedLanguage
from execution_pipeline.llm_executors.python_chatgpt import PythonChatGptExecutor
from execution_pipeline.llm_executors.python_langchain import PythonLangchainExecutor
from execution_pipeline.pipelines.default_pipeline import DefaultPipeline
from execution_pipeline.task_runners.default_task_runner import DefaultTaskRunner
from writer import write_test_results

llm_infos = [
    [OpenAI(temperature=0), "openai", True],
    [OpenAI(temperature=0, model_name="text-davinci-002"), "openai_davinci-002", True],
]

python_llm_executors = [
    *[PythonLangchainExecutor(*llm_info) for llm_info in llm_infos],
    PythonChatGptExecutor(model_name="gpt-3.5-turbo"),
    PythonChatGptExecutor(model_name="gpt-4"),
]

code_executor_mapping = {SupportedLanguage.PYTHON: PythonExecutor()}
llm_executor_mapping = {SupportedLanguage.PYTHON: python_llm_executors}

task_runner = DefaultTaskRunner(code_executor_mapping, llm_executor_mapping, StrippedExactMatch())

print("Running pipeline...")
results = asyncio.run(DefaultPipeline(task_runner).run())
print("Writing results...")
write_test_results(results, paths.root_path.joinpath('results/result.json'))
print("Done!")
