# syntax=docker/dockerfile:1
ARG base=tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

FROM ${base} AS build-fontrules
WORKDIR /src/langfontfinder
# Bring in selected context.
COPY --link scripts scripts
COPY --link lib lib
COPY --link data data
# Download langtags module, unzip and place module into lib.
ADD --link https://github.com/silnrsi/langtags/archive/refs/heads/master.zip langtags.zip
RUN python3 -m zipfile -e langtags.zip ./ && mv langtags-master/lib/langtag lib/
# Download source data and unzip for fontrules: SLDR & langtags.json
ADD --link https://github.com/silnrsi/sldr/archive/refs/heads/master.zip sldr.zip
RUN python3 -m zipfile -e sldr.zip ./ && mv sldr-master/sldr unflat
ADD --link https://ldml.api.sil.org/langtags.json lib/langtag/
# Generate fontrules.json
ENV PYTHONPATH=/src/findafont/lib
RUN <<EOT
    python3 scripts/fontrules \
        unflat/ \
        --fallbacks=data/script2font.csv \
        --outfile=data/fontrules.json
EOT

FROM ${base} AS runtime
LABEL org.opencontainers.image.source=https://github.com/silnrsi/langfontfinder
LABEL org.opencontainers.image.description="Language-Font-Finder REST API endpoint service"
LABEL org.opencontainers.image.licenses=MIT
# Download or copy service static data.
ADD --link --chmod=755 https://raw.githubusercontent.com/silnrsi/fonts/main/families.json /svc/data/
COPY --link --chmod=755 --from=build-fontrules /src/findafont/lib /app
COPY --link --chmod=755 --from=build-fontrules /src/findafont/data/ /svc/data/
ENV LFFPATH='/svc/data/' MODULE_NAME='langfontfinder.api' VARIABLE_NAME='lffapp' LANGTAGSPATH=/app/langtag/langtags.json
