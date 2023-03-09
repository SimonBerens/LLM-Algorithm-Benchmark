from execution_pipeline.languages import SupportedLanguage
from execution_pipeline.types import Task, TestResult, SubtestResult, Executor, TaskRunner


class DefaultTaskRunner(TaskRunner):
    def __init__(self, code_executor_mapping: dict[SupportedLanguage, Executor],
                 llm_executor_mapping: dict[SupportedLanguage, list[Executor]], evaluator):
        self.code_executor_mapping = code_executor_mapping
        self.llm_executor_mapping = llm_executor_mapping
        self.evaluator = evaluator

    def run(self, task: Task) -> TestResult:
        subtests = []
        for code_file in task.code_files:
            code_execution_results = self.code_executor_mapping[code_file.lang].execute(code_file.path,
                                                                                        task.input_paths)
            per_llm_execution_results = map(lambda llm_executor: llm_executor.execute(code_file.path, task.input_paths),
                                            self.llm_executor_mapping[code_file.lang])
            for llm_executor_index, llm_execution_results in enumerate(per_llm_execution_results):
                for input_path, code_execution_result, llm_execution_result in zip(task.input_paths,
                                                                                   code_execution_results,
                                                                                   llm_execution_results):
                    correctly_predicted = self.evaluator.is_valid(code_execution_result, llm_execution_result)
                    subtest = SubtestResult(language=code_file.lang, input_path=input_path,
                                            code_path=code_file.path,
                                            llm_executor=self.llm_executor_mapping[code_file.lang][llm_executor_index],
                                            predicted_output=llm_execution_result,
                                            code_output=code_execution_result,
                                            correctly_predicted=correctly_predicted)
                    subtests.append(subtest)

        num_correctly_predicted = sum(map(lambda subtest: subtest.correctly_predicted, subtests))
        num_failed = len(subtests) - num_correctly_predicted
        return TestResult(path=task.dir_path, metadata=task.metadata, subtest_results=subtests,
                          num_correctly_predicted=num_correctly_predicted, num_failed=num_failed)
