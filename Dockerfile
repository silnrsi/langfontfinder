# syntax=docker/dockerfile:1
ARG base=tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

FROM ${base} AS build-fontrules
ARG langtags_zip=https://github.com/silnrsi/langtags/archive/refs/heads/release.zip
ARG sldr_zip=https://github.com/silnrsi/sldr/archive/refs/heads/master.zip
ARG langtags_json=https://ldml.api.sil.org/langtags.json?staging=1
WORKDIR /src/langfontfinder
# Bring in selected context.
COPY --link scripts scripts
COPY --link lib lib
COPY --link data data
# Download langtags module, unzip and place module into lib.
ADD --link ${langtags_zip} langtags.zip
RUN python3 -m zipfile -e langtags.zip ./ && mv langtags-*/lib/langtag lib/
# Download source data and unzip for fontrules: SLDR & langtags.json
ADD --link ${sldr_zip} sldr.zip
RUN python3 -m zipfile -e sldr.zip ./ && mv sldr-*/sldr unflat
ADD --link ${langtags_json} lib/langtag/
# Generate fontrules.json
ENV PYTHONPATH=/src/langfontfinder/lib
RUN <<EOT
    python3 scripts/fontrules \
        unflat/ \
        --fallbacks=data/fallback.json \
        --outfile=data/fontrules.json
EOT

FROM ${base} AS runtime
LABEL org.opencontainers.image.source=https://github.com/silnrsi/langfontfinder
LABEL org.opencontainers.image.description="Language-Font-Finder REST API endpoint service"
LABEL org.opencontainers.image.licenses=MIT
# Download or copy service static data.
ADD --link --chmod=755 https://raw.githubusercontent.com/silnrsi/fonts/main/families.json /svc/data/
COPY --link --chmod=755 --from=build-fontrules /src/langfontfinder/lib /app
COPY --link --chmod=755 --from=build-fontrules /src/langfontfinder/data/ /svc/data/
ENV LFFPATH='/svc/data/' MODULE_NAME='langfontfinder.api' VARIABLE_NAME='lffapp' LANGTAGSPATH=/app/langtag/langtags.json
