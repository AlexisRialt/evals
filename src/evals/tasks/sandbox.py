"""Sandboxed agent eval.

Runs inside a Docker sandbox built from the repo's ``Dockerfile`` (via
``compose.yaml``). The model is given ``bash`` and ``python`` tools that
execute inside the container and must compute each answer rather than recall
it. Answers are exact-string targets, so scoring is a substring ``includes``
check against the submitted value.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.scorer import includes
from inspect_ai.solver import basic_agent, use_tools
from inspect_ai.tool import bash, python
from inspect_ai.util import SandboxEnvironmentSpec

from evals import DATASETS_DIR, PROJECT_ROOT

# Reuse the repo Dockerfile as the sample environment. The compose file lives
# at the repo root next to the Dockerfile; pass an absolute path so the task
# resolves regardless of the current working directory.
SANDBOX = SandboxEnvironmentSpec(
    type="docker",
    config=str(PROJECT_ROOT / "compose.yaml"),
)


@task
def sandbox_agent() -> Task:
    return Task(
        dataset=json_dataset(str(DATASETS_DIR / "inspect_ai_sandbox_tasks.jsonl")),
        solver=basic_agent(
            init=use_tools([bash(timeout=60), python(timeout=60)]),
            message_limit=15,
        ),
        scorer=includes(),
        sandbox=SANDBOX,
    )
