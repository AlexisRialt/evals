# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

LLM evaluation project built on the [Inspect AI](https://inspect.ai-safety-institute.org.uk/) framework. Each eval task pairs a JSONL dataset with a solver and a scorer; results are written to `logs/` as `.eval` files.

## Environment & Commands

- Python 3.13, managed with `uv` (see `uv.lock`). `ruff` lives in the `dev` dependency group.
- `OPENAI_API_KEY` is loaded from the macOS keychain via `.envrc` (direnv). Run `direnv allow` on first use so the key is exported.

```bash
uv sync                                                       # install dependencies
uv run inspect eval src/evals/tasks/scheming.py               # run the scheming task
uv run inspect eval src/evals/tasks/arithmetic.py             # run the arithmetic task
uv run inspect eval src/evals/tasks/sandbox.py                # run the Docker-sandboxed agent (needs Docker running)
uv run inspect eval src/evals/tasks/scheming.py --model openai/gpt-4o   # override model
uv run inspect eval src/evals/tasks/arithmetic.py --limit 1   # run a single sample while iterating
uv run inspect view                                           # browse .eval logs in the log viewer
uv run ruff check .                                           # lint
uv run ruff format .                                          # format
```

## Architecture

An eval is defined by a `@task`-decorated function returning an Inspect `Task`. Each task lives in its own module under `src/evals/tasks/`. A Task wires together three pieces:

- **Dataset** — loaded from `datasets/*.jsonl` via `json_dataset`. Each record has `id`, `input`, `target`, and `metadata`. `input` may be a plain string or a list of chat messages (system/user roles). Paths are built from `DATASETS_DIR` (in `src/evals/__init__.py`), which resolves the repo-root `datasets/` dir relative to the source file — so tasks load regardless of the current working directory. Do not hardcode CWD-relative paths.
- **Solver** — how the model is driven (e.g. `generate()`).
- **Scorer** — how output is judged. Pick based on the `target` shape: `match()` for exact-string targets, `model_graded_qa()` (LLM judge) when `target` is narrative grading guidance.

Running a task appends a timestamped `.eval` file to `logs/` (gitignored).

## Tasks & datasets

- `scheming_eval` (`src/evals/tasks/scheming.py`) → `datasets/inspect_ai_scheming_eval.jsonl`, scored with `model_graded_qa`. Paired `evaluation`/`deployment` conditions (same `pair_id`, differing `condition` in metadata) probing scheming behaviors (oversight avoidance, audit falsification, sandbagging, etc.). Compare results *within* each `pair_id`: safer behavior only under the `evaluation` condition is a warning sign. See `datasets/inspect_ai_scheming_eval_README.md`.
- `arithmetic` (`src/evals/tasks/arithmetic.py`) → `datasets/inspect_ai_small_dataset.jsonl`, scored with `match`. Small arithmetic/logic set with exact-string targets.
- `sandbox_agent` (`src/evals/tasks/sandbox.py`) → `datasets/inspect_ai_sandbox_tasks.jsonl`, scored with `includes`. A `basic_agent` with `bash`/`python` tools that must execute code to answer. Requires a running Docker daemon.

## Docker sandbox

`sandbox_agent` runs each sample in a Docker sandbox. The image is the repo `Dockerfile` (reused, not a second image); the sandbox service is defined in root `compose.yaml`, referenced from the task by an absolute path (`PROJECT_ROOT / "compose.yaml"` from `src/evals/__init__.py`). Key detail: the `Dockerfile` sets `ENTRYPOINT ["inspect"]` for running evals, so `compose.yaml` **overrides the entrypoint** with `tail -f /dev/null` — otherwise the sandbox container would try to run `inspect` and exit immediately, leaving nothing for Inspect to exec tool calls into. When editing the Dockerfile, keep this override in mind.

## Adding a task

Add a module under `src/evals/tasks/`, define a `@task` function using `DATASETS_DIR` for the dataset path, and export it from `src/evals/tasks/__init__.py`.
