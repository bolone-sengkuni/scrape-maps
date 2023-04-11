import json
import glob
import os
import time
import random
import string
import secrets

DIR = os.path.dirname(os.path.abspath(__file__))

from pprint import pprint

from jsonmerge import merge




result = []
for f in glob.glob(f"{DIR}/data/Bangkalan/libs/*.json"):
    print(f)
    with open(f, "rb") as infile:
        result.append(json.load(infile))

with open('ajaj.json', "w") as ass:
    json.dump(result, ass, indent=4)


