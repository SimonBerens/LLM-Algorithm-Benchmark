from abc import ABC
from dataclasses import dataclass
from pathlib import Path

from execution_pipeline.languages import SupportedLanguage


@dataclass
class SubtestResult:
    input_path: Path
    language: SupportedLanguage
    code_path: Path
    predicted_output: str
    generated_output: str
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


class Executor(ABC):
    def execute(self, code_path: Path, input_paths: list[Path]) -> list[str]:
        pass


class TaskRunner(ABC):
    def run(self, task: Task) -> TestResult:
        pass
