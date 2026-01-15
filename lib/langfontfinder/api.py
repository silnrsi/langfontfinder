#!/usr/bin/env python3

import sys, os, time
from fastapi import FastAPI, Response, Path
import uvicorn

try:
    from langfontfinder import LFF
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
    from langfontfinder import LFF

version = "0.2"
gitid = "$Id$"

datadir = os.getenv(
    "LFFPATH", os.path.join(os.path.dirname(__file__), "..", "..", "testdata")
)
rulesfile = os.getenv("LFFRULES", os.path.join(datadir, "fontrules.json"))
familiesfile = os.getenv("LFFFONTS", os.path.join(datadir, "families.json"))

ruleset = LFF(rulesfile, familiesfile)

__status = {
    "version": version, 
    # Use '\x24' instead of '$' here to prevent the git ident attribute from eating the everthing between them.
    "gitid": gitid.removeprefix("\x24Id: ").removesuffix(" \x24"),
    "families": len(ruleset.fontmap),
    "rules": {
        "generated": time.strftime("%a %d %b %H:%M:%S UTC %Y", time.gmtime(os.stat(rulesfile).st_mtime))
    },
    "langtags": { 
        "date": ruleset.langtags._info['version']['date'],
        "api": ruleset.langtags._info['version']['api']
    }
}


lffapp = FastAPI(version=version)

@lffapp.get("/lang/{ltag}", summary="lang/{ltag}", name="lang")
async def lang(response: Response, ltag: str = Path(description="Language tag")):
    """ Given a language tag, returns font location information as json object. """
    res = ruleset.get(ltag)
    if res is None:
        response.status_code = 404
    return res

@lffapp.get("/family/{familyid}", summary="family/{familyid}", name="family")
async def family(response:Response, familyid: str = Path(description="Font family id")):
    """ Given a familyid returns the font family json object. """
    res = ruleset.getfamily(familyid)
    if res is None:
        response.status_code = 404
    return res

@lffapp.get("/status")
async def status():
    return __status

if __name__ == "__main__":
    uvicorn.run(lffapp)
