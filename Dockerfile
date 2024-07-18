ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION} as python

# 'build' stage -------------------------------------------------------------------------------
FROM python as build-stage

RUN apt-get update \
  && apt-get install -y build-essential \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
# Install python packages
RUN pip install poetry==1.8.3 wheel==0.43.0
COPY ./pyproject.toml ./poetry.lock /
RUN poetry export --without-hashes --with-credentials --format requirements.txt --output requirements.txt
RUN pip wheel --wheel-dir /usr/src/app/wheels -r /requirements.txt

# 'run' stage --------------------------------------------------------------------------------
FROM python as run-stage
ARG APP_HOME=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONWARNINGS=ignore
# Copy python dependency wheels from build-stage
COPY --from=build-stage /usr/src/app/wheels /wheels/
# Use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && rm -rf /wheels
# Copy source code to WORKDIR
WORKDIR $APP_HOME
COPY app "${APP_HOME}"

# 'local' stage -------------------------------------------------------------------------------
FROM run-stage as local-stage
CMD ["python", "app"]
