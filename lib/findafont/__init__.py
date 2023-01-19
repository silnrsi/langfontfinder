#1/usr/bin/python3

from langtag import LangTags, LangTag, langtag
import json

class FaF:
    def __init__(self, rfile, ffile, ltags=None):
        self.langtags = LangTags(fname=ltags)
        with open(ffile, encoding="utf-8") as inf:
            self.fontmap = json.load(inf)
        with open(rfile, encoding="utf-8") as inf:
            rules = json.load(inf)
        self.scripts = [{}, [{}, [{}, None]]]
        for r in rules:
            m = r.get('match', None)
            if m is None:
                continue
            o = r.get('result', None)

            s = m.get('scr', None)
            if s is None:
                regrules = [self.scripts[1]]
            elif isinstance(s, list):
                regrules = [self.scripts[0].setdefault(x, [{}, [{}, None]]) for x in s]
            else:
                regrules = [self.scripts[0].setdefault(s, [{}, [{}, None]])]

            reg = m.get('reg', None)
            if reg is None:
                langrules = [x[1] for x in regrules]
            elif isinstance(reg, list):
                langrules = []
                for x in reg:
                    t = [y[0].setdefault(x, [{}, None]) for y in regrules]
                    langrules.extend(t)
            else:
                langrules = [x[0].setdefault(reg, [{}, None]) for x in regrules]

            lng = m.get('lang', None)
            if lng is None:
                for x in langrules:
                    if x[1] is None:
                        x[1] = o
            elif isinstance(lng, list):
                for l in lng:
                    for lr in langrules:
                        lr[0][l] = o
            else:
                for lr in langrules:
                    lr[0][lng] = o

    def getlt(self, txt):
        return self.langtags.get(str(txt), default=None)

    def _getmatch(self, lng, scr, reg, regrules):
        lngrules = regrules[0].get(reg, regrules[1])
        res = lngrules[0].get(lng, lngrules[1])
        if res is None:
            lngrules = regrules[1]
            if lngrules is not None:
                res = lngrules[0].get(lng, lngrules[1])
        return res

    def match(self, lng, scr, reg):
        res = self._getmatch(lng, scr, reg, self.scripts[0].get(scr, self.scripts[1]))
        if res is None:
            res = self._getmatch(lng, scr, reg, self.scripts[1])
        return res

    def getfamilyresult(self, matchres):
        familyid = matchres['familyid']
        family = self.fontmap.get(familyid, {})
        family.update(matchres)
        res = {'defaultfamily': [familyid], 'apiversion': 0.3, 'families': {familyid: family}}
        return res

    def get(self, ltag: str):
        if (lt := self.getlt(ltag)) is None:
            nlt = langtag(ltag)
            if nlt.region is not None:
                test = LangTag(nlt.lang, nlt.script, None, nlt.vars, nlt.ns)
                tr = self.getlt(str(test))
                if tr is not None:
                    lt = LangTag(tr.lang, tr.script, nlt.region, tr.vars, tr.ns)
            if lt is None and nlt.script is not None:
                test = LangTag(nlt.lang, None, nlt.region, nlt.vars, nlt.ns)
                tr = self.get(str(test))
                if tr is None:
                    test = LangTag(nlt.lang, None, None, nlt.vars, nlt.ns)
                    tr = self.getlt(str(test))
                    if tr is None:
                        test = LangTag(nlt.lang, None, None, None, None)
                        tr = self.getlt(str(test))
                if tr is not None:
                    lt = LangTag(tr.lang, nlt.script, nlt.region or tr.region, tr.vars, tr.ns)
        res = None
        if lt is not None:
            res = self.match(lt.lang, lt.script, lt.region)
            if res is not None:
                res = self.getfamilyresult(res)
        return res

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--rules",required=True,help="fontrules.json")
    parser.add_argument("-f","--fonts",required=True,help="families.json")
    parser.add_argument("-l","--lang",required=True,help="langtag")
    args = parser.parse_args()

    ruleset = FaF(args.rules, args.fonts)
    res = ruleset.get(args.lang)
    if res is not None:
        print(res)

if __name__ == "__main__":
    main()
