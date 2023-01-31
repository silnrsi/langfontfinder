# syntax=docker/dockerfile:1
ARG base=tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

FROM ${base} AS build-fontrules
WORKDIR /src/findafont
# Bring in selected context.
COPY --link scripts scripts
COPY --link lib lib
COPY --link data data
# Download langtags module, unzip and place module into lib.
ADD --link https://github.com/silnrsi/langtags/archive/refs/heads/master.zip langtags.zip
RUN python3 -m zipfile -e langtags.zip ./ && mv langtags-master/lib/langtag lib/
# Download source data and unzip for fontrules: SLDR & langtags.json
ARG sldr_path=sldr.zip
ADD --link ${sldr_path} ./sldr.zip
RUN python3 -m zipfile -e sldr.zip sldr
ADD --link https://ldml.api.sil.org/langtags.json lib/langtag/
# Generate fontrules.json
ENV PYTHONPATH=/src/findafont/lib
RUN <<EOT
    python3 scripts/fontrules \
        sldr/unflat/ \
        --fallbacks=data/script2font.csv \
        --outfile=data/fontrules.json
EOT

FROM ${base} AS runtime
# Download or copy service static data.
ADD --link --chmod=755 https://raw.githubusercontent.com/silnrsi/fonts/main/fonts/families.json /svc/data/
COPY --link --chmod=755 --from=build-fontrules /src/findafont/lib /app
COPY --link --chmod=755 --from=build-fontrules /src/findafont/data/ /svc/data/
ENV FAFPATH='/svc/data/' MODULE_NAME='findafont.api' VARIABLE_NAME='fafapp'
