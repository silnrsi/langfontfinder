#!/usr/bin/env python3

import sys, os, argparse
from fastapi import FastAPI, Response, Path
from fastapi.testclient import TestClient
import uvicorn

try:
    from findafont import FaF
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
    from findafont import FaF

version = "0.1"

datadir = os.getenv(
    "FAFPATH", os.path.join(os.path.dirname(__file__), "..", "..", "testdata")
)
rulesfile = os.getenv("FAFRULES", os.path.join(datadir, "fontrules.json"))
familiesfile = os.getenv("FAFFONTS", os.path.join(datadir, "families.json"))

# parser = argparse.ArgumentParser()
# parser.add_argument('-r','--rules',default=rulesfile,help='fontrules.json')
# parser.add_argument('-f','--fonts',default=familiesfile,help='families.json')
# args = parser.parse_args()

ruleset = FaF(rulesfile, familiesfile)

fafapp = FastAPI(version=version)


@fafapp.get("/lang/{ltag}", summary="lang/{ltag}", name="lang")
async def lang(response: Response, ltag: str = Path("", description="Language tag")):
    """ Given a language tag, returns font location information as json object. """
    res = ruleset.get(ltag)
    if res is None:
        response.status_code = 404
    return res


@fafapp.get("/status")
async def status():
    res = {"version": version}
    return res


if __name__ == "__main__":
    uvicorn.run(fafapp)
