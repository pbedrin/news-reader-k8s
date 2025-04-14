FROM python:3.11

RUN pip install poetry

WORKDIR /code

COPY pyproject.toml /code

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]