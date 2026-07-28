"""LLM evaluation tasks built on the Inspect AI framework."""

from pathlib import Path

# Repository root, resolved relative to this file so tasks locate their
# datasets and sandbox config regardless of the current working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASETS_DIR = PROJECT_ROOT / "datasets"

__all__ = ["DATASETS_DIR", "PROJECT_ROOT"]
