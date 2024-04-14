FROM python:3.11-slim

ENV WORKDIR /app

WORKDIR ${WORKDIR}

COPY . .

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-dev

EXPOSE 8080

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
