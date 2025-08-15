#!/usr/bin/python3
"""
API usage example:
- query a particular langtag via user input
- return 404 and error message if langtag is unknown
- access nested fields
- filter out some responses
"""

from pprint import pprint
import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("tag",nargs="?",help="Input language tag")
args = parser.parse_args()

if args.tag is None:
    args.tag = input("Pick your langtag (e.g. nod-Lana-TH wsg-Gong-IN shu-Arab-TD - tag-Script-REGION): ")

URL = "https://lff.api.languagetechnology.org/lang/"
fullURL = URL + args.tag
response = requests.get(fullURL)

if response.status_code == 200:
    data = json.loads(response.text)
    print("\nLFF API result for langtag: " + args.tag)
    for k, v in data["families"].items():
        print(f'family: {v["family"]}')
        print(f'version: {v["version"]}')
        print(f'source: {v["source"]}')
        print(f'distributable: {v["distributable"]}')
        print(f'license: {v["license"]}')
        print(f'status: {v["status"]}')
        print(f'download: {v["packageurl"]}')

        print("\nCSS @font-face URLs")

        for a in ("woff2", "woff", "ttf"):
            result = {
                n: f.get("flourl", f.get('url', None))
                for n, f in v.get("files", {}).items()
                if n.endswith(a)
                }
            result = {x: y for x, y in result.items() if y is not None}
            if len(result):
                pprint(result)
                break

else:
    print("Error: HTTP status code", response.status_code)
    print("\"" + args.tag + "\"" + " is not a known langtag")

