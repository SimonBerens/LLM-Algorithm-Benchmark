from execution_pipeline.languages import SupportedLanguage
from execution_pipeline.types import Task, TestResult, SubtestResult, Executor, TaskRunner


# todo move to executor mapping
# todo allow multiple llms

class DefaultTaskRunner(TaskRunner):
    def __init__(self, python_executor: Executor, python_llm_executor: Executor, evaluator):
        self.python_executor = python_executor
        self.python_llm_executor = python_llm_executor
        self.evaluator = evaluator

    def run(self, task: Task) -> TestResult:
        subtests = []
        for code_file in task.code_files:
            if code_file.lang == SupportedLanguage.PYTHON:
                execution_results = self.python_executor.execute(code_file.path, task.input_paths)
                generated_results = self.python_llm_executor.execute(code_file.path, task.input_paths)
                for input_path, execution_result, generated_result in zip(task.input_paths, execution_results,
                                                                          generated_results):
                    correctly_predicted = self.evaluator.is_valid(execution_result, generated_result)
                    subtest = SubtestResult(input_path=input_path,
                                            predicted_output=generated_result, language=SupportedLanguage.PYTHON,
                                            code_path=code_file.path,
                                            generated_output=execution_result,
                                            correctly_predicted=correctly_predicted)
                    subtests.append(subtest)

        num_correctly_predicted = sum(map(lambda x: x.correctly_predicted, subtests))
        num_failed = len(subtests) - num_correctly_predicted
        return TestResult(path=task.dir_path, metadata=task.metadata, subtest_results=subtests,
                          num_correctly_predicted=num_correctly_predicted, num_failed=num_failed)
