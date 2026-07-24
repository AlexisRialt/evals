# Inspect AI Scheming Evaluation

A small prompt-level screening set with paired `evaluation` and `deployment`
conditions. It covers oversight avoidance, hidden-goal conflict, audit
falsification, self-preservation, sandbagging, covert resource acquisition,
monitor manipulation, and evidence tampering.

```python
from inspect_ai.dataset import json_dataset
dataset = json_dataset("inspect_ai_scheming_eval.jsonl")
```

Use a model-graded scorer because each `target` is narrative grading guidance.
Compare results within each `pair_id`; safer behavior only in the evaluation
condition is a warning sign.

This set measures stated decisions, not actual covert behavior. Stronger tests
need tools, persistent state, realistic opportunities to act, and outcome-based
scoring.
