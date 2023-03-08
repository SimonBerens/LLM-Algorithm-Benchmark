from execution_pipeline.evaluators.stripped_exact_match import StrippedExactMatch
from execution_pipeline.language_exectuors.python_executor import PythonExecutor
from execution_pipeline.pipelines.default_pipeline import DefaultPipeline
from execution_pipeline.llm_executors.python_openai import OpenAiExecutor
from execution_pipeline.task_runners.default_task_runner import DefaultTaskRunner
from pprint import pprint
task_runner = DefaultTaskRunner(PythonExecutor(), OpenAiExecutor(), StrippedExactMatch())

results = DefaultPipeline(task_runner).run()

pprint(results)