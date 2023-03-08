from pprint import pprint

from execution_pipeline.code_exectuors.python_executor import PythonExecutor
from execution_pipeline.evaluators.stripped_exact_match import StrippedExactMatch
from execution_pipeline.languages import SupportedLanguage
from execution_pipeline.llm_executors.python_openai import PythonOpenAiExecutor
from execution_pipeline.pipelines.default_pipeline import DefaultPipeline
from execution_pipeline.task_runners.default_task_runner import DefaultTaskRunner

code_executor_mapping = {SupportedLanguage.PYTHON: PythonExecutor()}
llm_executor_mapping = {SupportedLanguage.PYTHON: PythonOpenAiExecutor()}

task_runner = DefaultTaskRunner(code_executor_mapping, llm_executor_mapping, StrippedExactMatch())

results = DefaultPipeline(task_runner).run()

pprint(results)
