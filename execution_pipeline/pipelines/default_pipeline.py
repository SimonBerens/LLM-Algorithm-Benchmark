import json
from asyncio import gather

from execution_pipeline.languages import get_language
from execution_pipeline.types import CodeFile, Task, TestResult, TaskRunner
from paths import tasks_path


class DefaultPipeline:
    def __init__(self, task_runner: TaskRunner):
        self.task_runner = task_runner

    async def run(self) -> list[TestResult]:
        tasks = []

        for task_dir in tasks_path.iterdir():
            input_paths = list(task_dir.joinpath('inputs').iterdir())
            with open(task_dir.joinpath("metadata.json"), "r") as subprocess_input:
                metadata = json.load(subprocess_input)
            code_files = [CodeFile(lang=get_language(code_file), path=code_file) for code_file in task_dir.joinpath('code').iterdir()]
            tasks.append(
                Task(dir_path=task_dir, input_paths=input_paths, code_files=code_files,
                     metadata=metadata))

        test_results = list(await gather(*map(self.task_runner.run, tasks)))

        return test_results
