from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from execution_pipeline.languages import SupportedLanguage


class Executor(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def execute(self, code_path: Path, input_paths: list[Path]) -> list[str]:
        pass


@dataclass
class SubtestResult:
    language: SupportedLanguage
    input_path: Path
    code_path: Path
    llm_executor: Executor
    predicted_output: str
    code_output: str
    correctly_predicted: bool


@dataclass
class TestResult:
    path: Path
    metadata: dict
    subtest_results: list[SubtestResult]
    num_correctly_predicted: int
    num_failed: int


@dataclass
class CodeFile:
    path: Path
    lang: SupportedLanguage


@dataclass
class Task:
    dir_path: Path
    input_paths: list[Path]
    code_files: list[CodeFile]
    metadata: dict


class TaskRunner(ABC):
    @abstractmethod
    async def run(self, task: Task) -> TestResult:
        pass
