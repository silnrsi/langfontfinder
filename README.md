# Find a Font Service

This project provides a micro service responder when passed language tag will
return information on a possible font to use for the orthography for that
language tag.

The API is built on top of FastAPI and runs using uvicorn.

To run:

```
python3 lib/findafont/api.py
```

After starting the service, queries are of the form lang/<langtag> as in:

```
http://127.0.0.1:8000/lang/en
```

There are standalone testing programs in the test/ directory.

Other endpoints are:

status/     Returns a simple version as a JSON object
docs/       FastAPI OpenAPI base documentation

