ARG TAG
FROM ghcr.io/deephaven/grpc-api:${TAG}

COPY app.d/ /app.d

RUN pip install watchdog