"""Inspect AI eval tasks."""

from evals.tasks.arithmetic import arithmetic
from evals.tasks.sandbox import sandbox_agent
from evals.tasks.scheming import scheming_eval

__all__ = ["arithmetic", "sandbox_agent", "scheming_eval"]
