# syntax=docker/dockerfile:1
FROM feastdev/feature-server:dev
WORKDIR /feast

COPY feature_repo/feature_store.yaml feature_store.yaml
RUN feast apply 

EXPOSE 6566

CMD ["feast", "serve", "--host=0.0.0.0", "--registry_ttl_sec=1"]