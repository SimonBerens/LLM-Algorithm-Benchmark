import json

from execution_pipeline.languages import get_language
from execution_pipeline.types import CodeFile, Task, TestResult, TaskRunner
from paths import tasks_path

class DefaultPipeline:
    def __init__(self, task_runner: TaskRunner):
        self.task_runner = task_runner

    def run(self) -> list[TestResult]:
        tasks = []

        for code_dir in tasks_path.glob('*/code'):
            input_paths = list(code_dir.parent.joinpath('inputs').iterdir())
            with open(code_dir.parent.joinpath("metadata.json"), "r") as subprocess_input:
                metadata = json.load(subprocess_input)
            code_files = [CodeFile(lang=get_language(code_file), path=code_file) for code_file in code_dir.iterdir()]
            tasks.append(
                Task(dir_path=code_dir, input_paths=input_paths, code_files=code_files,
                     metadata=metadata))

        test_results = list(map(self.task_runner.run, tasks))

        return test_results
