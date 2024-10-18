ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION} as python

# 'build' stage -------------------------------------------------------------------------------
FROM python as build-stage

RUN apt-get _update \
  && apt-get install -y build-essential \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Install python packages
COPY ./pyproject.toml ./poetry.lock /
COPY app /app
RUN pip install poetry==1.8.3
RUN poetry build --format=wheel

# 'run' stage --------------------------------------------------------------------------------
FROM python as run-stage
ARG APP_HOME=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONWARNINGS=ignore
# Copy python dependency wheels from build-stage
COPY --from=build-stage /dist/ /wheels/
# Use wheels to install python dependencies
RUN pip install --no-cache-dir --find-links=/wheels/ /wheels/* && rm -rf /wheels

# 'local' stage -------------------------------------------------------------------------------
FROM run-stage as local-stage
CMD ["python", "app/adapters/api"]
