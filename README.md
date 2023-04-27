# Find a Font Service

This project provides a micro service responder when passed language tag will
return information on a possible font to use for the orthography for that
language tag.

Details of the returned JSON object may be found [here](docs/results.md).

## Usage

The service has the following endpoints available:
| Endpoint | Description                                    |
| ------------ | ------------------------------------------ |
| lang/_langtag_ | Returns a json object of the font for the langtag |
| family/_familyid_ | Returns a json object of just the font family record for the family |
| status/ |    Returns a simple version as a JSON object    |
| docs/   |    FastAPI OpenAPI base documentation (Swagger) |
| redoc/  |    Prettier OpenAPI base documentation (ReDoc)  |
| openapi.json | OpenAPI schema in JSON                     |


## Startup

The API is built on top of FastAPI and runs using uvicorn.

To run:

```
python3 lib/findafont/api.py
```

There are standalone testing programs in the test/ directory.
