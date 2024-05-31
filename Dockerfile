#
# MIT License
#
# (C) Copyright 2024 Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
## Cray Secure Token Service Dockerfile
## Copyright 2019-2021 Hewlett Packard Enterprise Development LP

FROM artifactory.algol60.net/docker.io/alpine:3.18 as base

RUN apk add --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --upgrade pip setuptools wheel gunicorn==20.1.0

ENV STS_RUNTIME "container"
ENV STS_ENV "development"

FROM base as build

RUN mkdir -p /build
COPY . /build
WORKDIR /build

RUN python setup.py sdist bdist_wheel

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
