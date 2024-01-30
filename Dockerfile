FROM python:3.12.1-slim-bullseye as base
WORKDIR /src

FROM base as builder
ENV POETRY_VERSION=1.7.1
COPY pyproject.toml poetry.lock ./
RUN pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi

FROM base as final
COPY ./app ./app
COPY --from=builder /src/.venv /src/.venv

CMD .venv/bin/python app/manage.py runserver 0.0.0.0:$PORT --noreload
