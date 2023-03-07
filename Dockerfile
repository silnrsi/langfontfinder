# syntax=docker/dockerfile:1
ARG base=tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

FROM python:3.11 AS build-fontrules
WORKDIR /src/findafont
# Bring in selected context.
COPY --link scripts scripts
COPY --link lib lib
COPY --link data data
COPY --link requirements.txt requirements.txt
# Download source data and unzip for fontrules: SLDR & langtags.json
ADD --link https://github.com/silnrsi/sldr/archive/refs/heads/master.zip sldr.zip
RUN unzip sldr.zip sldr-master/sldr/*
ADD --link https://ldml.api.sil.org/langtags.json data/
# Generate fontrules.json
ENV PYTHONPATH=/src/findafont/lib LANGTAGSPATH=/src/findafont/data/langtags.json
RUN <<EOT
    pip install uvicorn[standard] fastapi[all] -r requirements.txt
    python3 scripts/fontrules \
        sldr-master/sldr \
        --fallbacks=data/script2font.csv \
        --outfile=data/fontrules.json
EOT

FROM python:3.11-slim AS runtime
LABEL org.opencontainers.image.source=https://github.com/silnrsi/findafont
LABEL org.opencontainers.image.description="Find-a-Font REST API endpoint service"
LABEL org.opencontainers.image.licenses=MIT
# Download or copy service static data.
ADD --link --chmod=755 https://raw.githubusercontent.com/silnrsi/fonts/main/families.json /svc/data/
COPY --link --from=build-fontrules /usr/local/lib/python3.11/site-packages  /usr/local/lib/python3.11/site-packages
COPY --link --from=build-fontrules /usr/local/bin/ /usr/local/bin/
COPY --link --chmod=755 --from=build-fontrules /src/findafont/data/ /svc/data/
COPY --link --chmod=755 --from=build-fontrules /src/findafont/lib /app
ENV FAFPATH='/svc/data/' LANGTAGSPATH='/svc/data/langtags.json' PYTHONPATH='/app'
CMD ["uvicorn", "findafont.api:fafapp", "--host","0.0.0.0", "--port", "80"]
