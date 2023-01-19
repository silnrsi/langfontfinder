import sys, os, argparse
from fastapi import FastAPI, Response
from fastapi.testclient import TestClient
import uvicorn

try:
    from findafont import FaF
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
    from findafont import FaF

datadir = os.getenv('FAFPATH', os.path.join(os.path.dirname(__file__), '..', '..', 'testdata'))
rulesfile = os.getenv('FAFRULES', os.path.join(datadir, 'fontrules.json'))
familiesfile = os.getenv('FAFFONTS', os.path.join(datadir, 'families.json'))
ltfile = os.getenv('FAFLANGTAGS', os.path.join(datadir, 'langtags.json'))

#parser = argparse.ArgumentParser()
#parser.add_argument('-r','--rules',default=rulesfile,help='fontrules.json')
#parser.add_argument('-f','--fonts',default=familiesfile,help='families.json')
#parser.add_argument('-l','--langs',default=ltfile,help='langtags.json')
#args = parser.parse_args()

ruleset = FaF(rulesfile, familiesfile, ltags=ltfile)

fafapp = FastAPI()

@fafapp.get("/lang/{ltag}")
async def getfromlt(ltag: str, response: Response):
    res = ruleset.get(ltag)
    if res is None:
        response.status_code = 404
    return res

if __name__ == "__main__":
    uvicorn.run(fafapp)
