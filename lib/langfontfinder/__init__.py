#!/usr/bin/env python3

from langtag import LangTags, LangTag, langtag
import json


class LFF:
    def __init__(self, rfile, ffile=None, ltags=None):
        self.langtags = LangTags(fname=ltags)
        if ffile is not None:
            with open(ffile, encoding="utf-8") as inf:
                self.fontmap = json.load(inf)
        else:
            self.fontmap = {}
        with open(rfile, encoding="utf-8") as inf:
            rules = json.load(inf)
        self.varrules = rules["variants"]
        self.lngrules = rules["langs"]
        self.regrules = rules["regions"]
        self.scrrules = rules["scripts"][0]

    def getlt(self, txt):
        """returns a language tag tagset for the given textual language tag"""
        try:
            return self.langtags.get(str(txt), default=None)
        except SyntaxError:
            return None

    def _getmatch(self, lng, scr, reg, var, regnum):
        regrules = self.regrules[regnum]
        lngrules = self.lngrules[regrules[1].get(reg, regrules[0])]
        varrules = self.varrules[lngrules[1].get(lng, lngrules[0])]
        res = varrules[1].get(var, varrules[0])
        return res

    def match(self, lng, scr, reg, var):
        """Given broken out lang tag components, return the rule result that matches."""
        if scr is not None and len(scr) and scr not in self.scrrules[1]:
            return None         # bail on unknown script
        res = self._getmatch(
            lng, scr, reg, var, self.scrrules[1].get(scr, self.scrrules[0])
        )
        if res is None:
            res = self._getmatch(lng, scr, reg, var, self.scrrules[0])
        return res

    def getfamilyresult(self, matchres):
        """Given a rule result, merge with the fonts family information to give a full result."""
        allfamilies = set()
        for r, v in matchres['roles'].items():
            allfamilies.update([f for f in v if f in self.fontmap]))        # filter to only those we have font records for
        res = {'roles': matchres['roles']}
        defaults = res['roles'].get('default', None)
        if defaults is None:
            if len(res['roles']):
                defaults = res['roles'].items()[0][1]
            else:
                defaults = []
        res['defaultfamily'] = defaults
        res['apiversion'] = 0.3
        feats = matchres.get('features', {})
        if len(allfamilies):
            res['families'] = {}
            for f in allfamilies:
                family = self.fontmap.get(f, {}).copy()
                feat = feats.get(f, None)
                if feat is not None:
                    family['features'] = feat
                res['families'][f] = family
        return res

    def getfamily(self, familyid):
        return self.fontmap.get(familyid, None)

    def get(self, ltag: str):
        """Given a textual language tag return fully font family information for it."""
        if (lt := self.getlt(ltag)) is None:
            try:
                nlt = langtag(ltag)
            except SyntaxError:
                return None
            if nlt.region is not None:
                test = LangTag(nlt.lang, nlt.script, None, nlt.vars, nlt.ns)
                tr = self.getlt(str(test))
                if tr is not None:
                    lt = LangTag(tr.lang, tr.script, nlt.region, tr.vars, tr.ns)
            if lt is None and nlt.script is not None:
                test = LangTag(nlt.lang, None, nlt.region, nlt.vars, nlt.ns)
                tr = self.getlt(str(test))
                if tr is None:
                    test = LangTag(nlt.lang, None, None, nlt.vars, nlt.ns)
                    tr = self.getlt(str(test))
                    if tr is None:
                        test = LangTag(nlt.lang, None, None, None, None)
                        tr = self.getlt(str(test))
                if tr is not None:
                    lt = LangTag(
                        tr.lang, nlt.script, nlt.region or tr.region, tr.vars, tr.ns
                    )
            else:
                lt = nlt
        res = None
        if lt is not None and lt.lang is not None:
            var = []
            if lt.vars is not None and len(lt.vars):
                var.extend(lt.vars)
            if lt.ns is not None:
                for k in sorted(lt.ns.keys()):
                    var.extend([k.lower()] + lt.ns[k])
            res = self.match(lt.lang, lt.script, lt.region, "-".join(var) or None)
            if res is not None:
                res = self.getfamilyresult(res)
        return res


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rules", required=True, help="fontrules.json")
    parser.add_argument("-f", "--fonts", required=True, help="families.json")
    parser.add_argument("-l", "--lang", required=True, help="langtag")
    args = parser.parse_args()

    ruleset = LFF(args.rules, args.fonts)
    res = ruleset.get(args.lang)
    if res is not None:
        print(res)


if __name__ == "__main__":
    main()
