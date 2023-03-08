from enum import auto, Enum
from pathlib import Path


class SupportedLanguage(Enum):
    PYTHON = auto()


def get_language(file_name: Path):
    extension = file_name.suffix[1:]
    if extension == 'py':
        return SupportedLanguage.PYTHON
    else:
        raise ValueError
