from pathlib import Path


def force_write_to(path: Path, content: str):
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_text(content)
