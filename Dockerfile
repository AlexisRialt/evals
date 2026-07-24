# syntax=docker/dockerfile:1

# Uses the official uv image so the container toolchain matches local dev.
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Compile bytecode on install and copy (don't symlink) from the uv cache.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install dependencies in their own layer so they're cached across code changes.
COPY pyproject.toml uv.lock README.md ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Add the project source and install the package itself.
COPY src ./src
COPY datasets ./datasets
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Put the venv on PATH so `inspect` runs directly.
ENV PATH="/app/.venv/bin:$PATH"

# OPENAI_API_KEY must be provided at runtime, e.g.:
#   docker run --rm -e OPENAI_API_KEY -v "$PWD/logs:/app/logs" evals \
#     eval src/evals/tasks/arithmetic.py --model openai/gpt-4o-mini
ENTRYPOINT ["inspect"]
CMD ["eval", "src/evals/tasks/arithmetic.py"]
