from execution_pipeline.languages import SupportedLanguage
from execution_pipeline.types import Task, TestResult, SubtestResult, Executor, TaskRunner


# todo allow multiple llms

class DefaultTaskRunner(TaskRunner):
    def __init__(self, code_executor_mapping: dict[SupportedLanguage, Executor],
                 llm_executor_mapping: dict[SupportedLanguage, Executor], evaluator):
        self.code_executor_mapping = code_executor_mapping
        self.llm_executor_mapping = llm_executor_mapping
        self.evaluator = evaluator

    def run(self, task: Task) -> TestResult:
        subtests = []
        for code_file in task.code_files:
            execution_results = self.code_executor_mapping[code_file.lang].execute(code_file.path, task.input_paths)
            generated_results = self.llm_executor_mapping[code_file.lang].execute(code_file.path, task.input_paths)
            for input_path, execution_result, generated_result in zip(task.input_paths, execution_results,
                                                                      generated_results):
                correctly_predicted = self.evaluator.is_valid(execution_result, generated_result)
                subtest = SubtestResult(input_path=input_path,
                                        predicted_output=generated_result, language=code_file.lang,
                                        code_path=code_file.path,
                                        generated_output=execution_result,
                                        correctly_predicted=correctly_predicted)
                subtests.append(subtest)

        num_correctly_predicted = sum(map(lambda x: x.correctly_predicted, subtests))
        num_failed = len(subtests) - num_correctly_predicted
        return TestResult(path=task.dir_path, metadata=task.metadata, subtest_results=subtests,
                          num_correctly_predicted=num_correctly_predicted, num_failed=num_failed)
