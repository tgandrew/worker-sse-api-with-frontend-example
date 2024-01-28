FROM python:3.11

WORKDIR /workspace

COPY pyproject.toml ./
COPY poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY api.py ./
COPY worker.py ./