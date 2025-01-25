FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y \
    libmagic1 \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "hypercorn", "src/main:app", "--bind", "::"] 
