import json
import os

PATH = os.path.realpath(__file__)
DIRECTORY = os.path.dirname(PATH)
os.chdir(DIRECTORY)

def to_json(data, filename : str):
    with open(filename, 'w', encoding = 'utf-8') as f:
        json.dump(data, f, indent = 2)

def load_json(filename : str):
    with open(filename, 'r', encoding = 'utf-8') as f:
        return json.load(f)

questions = load_json('Set-ALL.json')
for q in questions:
    q['subject'] = q['subject'].strip()

to_json(questions, 'set.json')