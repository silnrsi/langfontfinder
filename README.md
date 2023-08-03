# Language Font Finder Service

This project provides a micro service responder when passed language tag will
return information on a possible font to use for the orthography for that
language tag.

Details of the returned JSON object may be found [here](docs/results.md).

## Access

The Language Font Finder service is available at [https://lff.api.languagetechnology.org/docs](https://lff.api.languagetechnology.org/docs).

## Usage

The service has the following endpoints available:
| Endpoint | Description                                    |
| ------------ | ------------------------------------------ |
| lang/_langtag_ | Returns a json object of the font for the BCP 47 _langtag_ |
| family/_familyid_ | Returns a json object of just the font family record for the family |
| status/ |    Returns a simple version as a JSON object    |
| docs/   |    FastAPI OpenAPI base documentation (Swagger) |
| redoc/  |    Prettier OpenAPI base documentation (ReDoc)  |
| openapi.json | OpenAPI schema in JSON                     |

## Examples

[https://lff.api.languagetechnology.org/lang/kfc](https://lff.api.languagetechnology.org/lang/kfc) returns a JSON object with information about a font that supports the Konda-Dora language (kfc) which is written with Telugu script (Telu).

[https://lff.api.languagetechnology.org/family/notoseriftibetan](https://lff.api.languagetechnology.org/family/notoseriftibetan) returns a JSON object with information about the Noto Serif Tibetan font family.

## Startup

The API is built on top of FastAPI and runs using uvicorn.

To run:

```
python3 lib/langfontfinder/api.py
```

There are standalone testing programs in the test/ directory.
