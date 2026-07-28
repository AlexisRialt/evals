# evals

LLM evaluation tasks built on the [Inspect AI](https://inspect.ai-safety-institute.org.uk/) framework.

Each task pairs a JSONL dataset with a solver and a scorer. Running a task appends a timestamped `.eval` file to `logs/`, which you can browse with the Inspect log viewer.

## Setup

Requires Python 3.13 and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync
```

Tasks call the OpenAI API and need `OPENAI_API_KEY` in the environment. This repo loads it from the macOS keychain via [`direnv`](https://direnv.net/) (see `.envrc`); run `direnv allow` once to enable it, or export the key yourself.

## Running

```bash
uv run inspect eval src/evals/tasks/arithmetic.py        # exact-match arithmetic/logic
uv run inspect eval src/evals/tasks/scheming.py          # model-graded scheming screen
uv run inspect eval src/evals/tasks/sandbox.py           # agent in a Docker sandbox (needs Docker)

uv run inspect eval src/evals/tasks/scheming.py --model openai/gpt-4o   # override the model
uv run inspect eval src/evals/tasks/arithmetic.py --limit 1             # single sample while iterating

uv run inspect view                                      # browse .eval logs
```

## Tasks

| Task            | Dataset                                | Scorer            |
| --------------- | -------------------------------------- | ----------------- |
| `arithmetic`    | `inspect_ai_small_dataset.jsonl`       | `match` (exact)   |
| `scheming_eval` | `inspect_ai_scheming_eval.jsonl`       | `model_graded_qa` |
| `sandbox_agent` | `inspect_ai_sandbox_tasks.jsonl`       | `includes`        |

**`scheming_eval`** screens for scheming behaviors (oversight avoidance, audit falsification, sandbagging, etc.) using paired `evaluation`/`deployment` prompts. Compare results *within* each `pair_id`: safer behavior only under the `evaluation` condition is a warning sign. Targets are narrative grading guidance, hence the LLM judge. See [datasets/inspect_ai_scheming_eval_README.md](datasets/inspect_ai_scheming_eval_README.md).

**`arithmetic`** is a small arithmetic/logic set with exact-string targets.

**`sandbox_agent`** runs a `basic_agent` with `bash`/`python` tools inside a Docker sandbox built from this repo's [Dockerfile](Dockerfile) (via [compose.yaml](compose.yaml)). The agent must *execute* code in the container to compute each answer. Requires a running Docker daemon.

## Layout

```
src/evals/tasks/   # one module per eval task
datasets/          # JSONL eval inputs
Dockerfile         # image, reused as the sandbox environment
compose.yaml       # sandbox service (overrides the image entrypoint to stay alive)
logs/              # .eval outputs (gitignored)
```

## Development

```bash
uv run ruff check .
uv run ruff format .
```

## License

[MIT](LICENSE)
