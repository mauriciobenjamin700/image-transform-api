FROM python:3.12-slim

WORKDIR /api

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml .
COPY uv.lock .


RUN uv sync --frozen --no-cache
RUN uv export --no-dev --no-hashes -o requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN rm pyproject.toml uv.lock requirements.txt

ENV PATH="/root/.local/bin:$PATH"

COPY logging_config.yaml .
COPY main.py .

COPY app ./app

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "120", "main:app"]
