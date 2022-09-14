"""
Helper functions
"""

import json

def load_json(js0n):
    with open(js0n) as json_file:
        return json.load(json_file)
