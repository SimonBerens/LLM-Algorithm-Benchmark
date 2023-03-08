import subprocess
from pathlib import Path

from execution_pipeline.types import Executor


class PythonExecutor(Executor):
    def __init__(self):
        pass

    def execute(self, code_path: Path, input_paths: list[Path]) -> list[str]:
        execution_results = []
        for input_path in input_paths:
            with open(input_path, "r") as f:
                subprocess_result = subprocess.run(["python", str(code_path)], stdin=f,
                                                   stdout=subprocess.PIPE,
                                                   encoding="utf-8")
                execution_results.append(subprocess_result.stdout)
        return execution_results
