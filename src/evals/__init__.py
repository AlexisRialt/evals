"""LLM evaluation tasks built on the Inspect AI framework."""

from pathlib import Path

# Repository-root ``datasets/`` directory, resolved relative to this file so
# tasks load their JSONL regardless of the current working directory.
DATASETS_DIR = Path(__file__).resolve().parents[2] / "datasets"

__all__ = ["DATASETS_DIR"]
