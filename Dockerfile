# syntax=docker/dockerfile:1
FROM python:3.11-alpine
WORKDIR /feast

COPY feature_repo/feature_store.yaml feature_store.yaml

RUN apk update && apk add --virtual build-dependencies build-base gcc cmake py3-pyarrow

RUN pip install pip --upgrade
RUN pip install "feast[redis, postgres, duckdb]"
RUN feast apply 

EXPOSE 8888

CMD ["feast", "ui", "--registry_ttl_sec=1"]