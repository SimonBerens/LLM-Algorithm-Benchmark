from asyncio import subprocess, gather
from functools import partial
from pathlib import Path

from execution_pipeline.types import Executor


async def execute_single_input(code_path: Path, input_path: Path) -> str:
    with open(input_path, "r") as f:
        subprocess_result = await subprocess.create_subprocess_exec(f"python", code_path, stdin=f,
                                                                    stdout=subprocess.PIPE)
        return (await subprocess_result.stdout.read()).decode('utf-8')


class PythonExecutor(Executor):
    @property
    def name(self) -> str:
        return "code_executor_python"

    def __init__(self):
        pass

    async def execute(self, code_path: Path, input_paths: list[Path]) -> list[str]:
        return list(await gather(*map(partial(execute_single_input, code_path), input_paths)))
