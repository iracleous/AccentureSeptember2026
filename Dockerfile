FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache -r pyproject.toml

COPY src ./src

RUN uv pip install --system --no-cache .

EXPOSE 8000

CMD ["uvicorn", "day11.agent:app", "--host", "0.0.0.0", "--port", "8000"]
