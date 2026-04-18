from __future__ import annotations

from pathlib import Path


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8")


def write_text_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
