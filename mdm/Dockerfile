ARG REPO
ARG BASE_IMAGE=python
ARG IMAGE_TAG=3.12-slim
FROM ${REPO}${BASE_IMAGE}:${IMAGE_TAG} AS requirements-step

ENV POETRY_VIRTUALENVS_CREATE=False
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"
RUN pip install "poetry<2" && poetry self add "poetry-plugin-export<1.9.0"
WORKDIR /tmp
ENV PATH="/root/.local/bin:$PATH"
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN  poetry export --only main --output requirements.txt --without-hashes
RUN  poetry export --with test --output test-requirements.txt --without-hashes

FROM requirements-step AS test

COPY ./pyproject.toml ./poetry.lock* ./
RUN  pip install -r test-requirements.txt
COPY ./mdm ./mdm
COPY ./tests ./tests
RUN mkdir -p /test-results
RUN pytest || touch /tmp/failed.tests
RUN cp results.xml /test-results/

FROM scratch AS test-results-exporter
COPY --from=test /test-results/* /tmp/

FROM test AS test-results-verifier
RUN if [ -f /test-results/failed.tests ]; then (echo "Tests Failed" && exit 1); fi

FROM ${REPO}${BASE_IMAGE}:${IMAGE_TAG} AS app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=True

# make sure to trigger test-results-verifier stage
COPY --from=test-results-verifier /tmp/*.dummy /tmp2/
RUN rm -rf /tmp2/

WORKDIR /code

RUN apt update && apt install -y \
    curl less zip unzip \
    && rm -rf /var/lib/apt/lists/*

RUN echo "alias ll='ls -la --color=auto'" >> /etc/bash.bashrc

COPY --from=requirements-step /tmp/requirements.txt ./
RUN  pip install -r requirements.txt
COPY ./mdm ./mdm

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


CMD [ "uvicorn", "mdm.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header" ]
