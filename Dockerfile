FROM node:20-alpine as develop-stage
WORKDIR /app
COPY package*.json ./
RUN yarn global add vite
COPY . .

FROM develop-stage as build-stage
RUN yarn
RUN yarn build

FROM python:3.11.9-slim as production-stage

EXPOSE 5000

RUN apt-get update && \
  apt-get install -y build-essential default-libmysqlclient-dev pkg-config && \
  rm -rf /var/lib/apt/lists/*
RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && \
  poetry install --no-root --no-interaction --no-ansi --without dev

COPY . /app
COPY --from=build-stage /app/vue/dist /app/vue/dist
