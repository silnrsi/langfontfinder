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

URL = "https://lff.api.languagetechnology.org/lang/"
lang = input("Pick your langtag (e.g. nod-Lana-TH wsg-Gong-IN shu-Arab-TD - tag-Script-REGION): ")
fullURL = URL + lang

response = requests.get(fullURL)

if response.status_code == 200:
    data = json.loads(response.text)
    for k, v in data["families"].items():
        print("\nLFF API result for langtag: " + lang)
        print(f'family: {v["family"]}')
        print(f'version: {v["version"]}')
        print(f'source: {v["source"]}')
        print(f'distributable: {v["distributable"]}')
        print(f'license: {v["license"]}')
        print(f'status: {v["status"]}')
        print(f'download: {v["packageurl"]}')

        print("\nCSS @font-face URLs (filtered for woff2 only)")

    result = {
        k: f["flourl"]
        for v in data["families"].values()
        for k, f in v["files"].items()
        if k.endswith("woff2")
        }
if response.status_code == 404:
    print("Error: HTTP status code", response.status_code)
    print("\"" + lang + "\"" + " is not a known langtag")

# examine the headers
# pprint(response.headers)

try:
    pprint(result)
except NameError:
    print("Sorry, no API result, try another langtag")
