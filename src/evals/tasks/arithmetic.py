"""Arithmetic and logic eval.

A small set with exact-string targets (e.g. ``"45"``, ``"yes"``), so it is
scored by string matching rather than an LLM judge.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.scorer import match
from inspect_ai.solver import generate

from evals import DATASETS_DIR


@task
def arithmetic() -> Task:
    return Task(
        dataset=json_dataset(str(DATASETS_DIR / "inspect_ai_small_dataset.jsonl")),
        solver=generate(),
        scorer=match(),
    )
