#!/usr/bin/python3
"""
API usage example:
- query a particular font via user input
- return 404 and error message if font is unknown
"""

import json
import requests

URL = "https://lff.api.languagetechnology.org/family/"
family = input("Pick your font family name (e.g. payaplanna): ")
fullURL = URL + family

response = requests.get(fullURL)

if response.status_code == 200:
    data = json.loads(response.text)
    print("\nLFF API result for font: " + family)
    for k in data:
        print(k, ":", data[k])

if response.status_code == 404:
    print("Error: HTTP status code", response.status_code)
    print('"' + family + '"' + " is not a known font family")
    print("Sorry, no API result, try another font family")
