import json
import os
PATH = os.path.realpath(__file__)
DIRECTORY = os.path.dirname(PATH)
os.chdir(DIRECTORY)


# questions = []
# for n in range(1, 17):
#    with open('Set-' + str(n) + '.json', 'r', encoding = 'utf-8') as f:
#         questions += json.load(f)

# with open('Set-ALL.json', 'w', encoding = 'utf-8') as f:
#     json.dump(questions, f, indent = 2)

with open('Set-ALL.json', 'r', encoding = 'utf-8') as f:
    questions = json.load(f)
    print(len(questions))