## Cray Secure Token Service Dockerfile
## Copyright 2019-2021 Hewlett Packard Enterprise Development LP

FROM artifactory.algol60.net/docker.io/alpine as base

RUN apk add --no-cache python3 && ln -sf python3 /usr/bin/python

ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m ensurepip
RUN pip3 install --upgrade pip setuptools wheel gunicorn==20.1.0 build

ENV STS_RUNTIME "container"
ENV STS_ENV "development"

FROM base as build

RUN mkdir -p /build
COPY . /build
WORKDIR /build

RUN python -m build --sdist --wheel /build

# TODO: uncomment once some tests are created
# FROM base as test

# RUN mkdir -p /app
# COPY . /app
# WORKDIR /app

# RUN apk add --no-cache gcc g++ musl-dev python3-dev
# RUN pip install nox

# RUN nox

FROM base as install

RUN mkdir -p /api
COPY ./api /api

RUN mkdir -p /install
COPY --from=build /build/dist/*.whl /install
RUN pip3 install /install/*.whl

CMD [ "gunicorn", "--bind=0.0.0.0:8000", "--workers=4", "sts.sts:conn_app" ]
