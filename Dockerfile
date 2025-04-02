FROM python:3.11
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN apt-get update && apt-get install -y build-essential

COPY pyproject.toml* poetry.lock* ./

RUN pip install --upgrade pip setuptools && pip install poetry==1.8.5 && poetry config virtualenvs.create false && poetry lock --no-update && poetry install

CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]