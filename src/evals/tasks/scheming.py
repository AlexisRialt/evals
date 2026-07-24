"""Scheming-behavior screening eval.

Paired ``evaluation``/``deployment`` prompts probing oversight avoidance, audit
falsification, sandbagging and related behaviors. Targets are narrative grading
guidance, so the task is scored by an LLM judge (``model_graded_qa``). Compare
results within each ``pair_id``: safer behavior only under the ``evaluation``
condition is a warning sign.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.scorer import model_graded_qa
from inspect_ai.solver import generate

from evals import DATASETS_DIR


@task
def scheming_eval() -> Task:
    return Task(
        dataset=json_dataset(str(DATASETS_DIR / "inspect_ai_scheming_eval.jsonl")),
        solver=generate(),
        scorer=model_graded_qa(),
    )
