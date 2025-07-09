FROM python:3.12-slim-bookworm as builder

WORKDIR /opt/remnashop

COPY pyproject.toml .
COPY docker-entrypoint.sh .

RUN pip install --no-cache-dir uv && \
    uv sync --system


FROM python:3.12-slim-bookworm

WORKDIR /opt/remnashop

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY . .

ENV UVICORN_RELOAD_ENABLED=false
ENV PYTHONUNBUFFERED=1

CMD [ "/bin/sh", "docker-entrypoint.sh" ]