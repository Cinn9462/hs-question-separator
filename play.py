# SESSIONS AUTOMATICALLY SAVE TO A JSON IN THE LOCAL DIRECTORY
# OVERRIDE COMMANDS ARE 'ADD' 'SUB' 'NULL' 'STOP'
# PARAMETERS FOR NEW GAME
SUBJECT = '5' # 1-Math, 2-Physics, 3-Chemistry, 4-Biology, 5-Earth and space
MIN_SET = 11 # 1 for no restrictions
MAX_SET = 16 # 16 for no restrictions
MIN_ROUND = 1 # 1 for no restrictions
MAX_ROUND = 17 # 17 for no restrictions

import os
import json
import random
from difflib import SequenceMatcher
import copy as c

# Set working directory as file directory
PATH = os.path.realpath(__file__)
DIRECTORY = os.path.dirname(PATH)
os.chdir(DIRECTORY)

SET = 'set.json'
SUBJECTS = {
    '1' : ['MATH'],
    '2' : ['PHYSICS'],
    '3' : ['CHEMISTRY'],
    '4' : ['BIOLOGY'],
    '5' : ['EARTH SCIENCE', 'ASTRONOMY', 'EARTH AND SPACE', 'EARTH & SPACE']
}

NEW_GAME = {
    'attempted' : 0,
    'incomplete' : None, # Stored as index of questions that are of the same subject
    'score' : 0,
    'min_set' : MIN_SET,
    'max_set' : MAX_SET,
    'min_round' : MIN_ROUND,
    'max_round' : MAX_ROUND,
    'subject' : SUBJECT # Stored as list of subjects
}

# Helper Functions
def check(question, s, min_s, min_r, max_s, max_r):
    return min_s <= int(question['set']) <= max_s and min_r <= int(question['round']) <= max_r and question['subject'].upper() in s

def to_json(data, filename : str):
    with open(filename, 'w', encoding = 'utf-8') as f:
        json.dump(data, f, indent = 2)

def load_json(filename : str):
    with open(filename, 'r', encoding = 'utf-8') as f:
        return json.load(f)

# Gameplay
questions = load_json(SET)

new = input('Would you like to start a new session [Y/N]\n')
print()

if new.lower() == 'y':
    session = c.deepcopy(NEW_GAME)

    subjects = []
    for n in session.get('subject'):
        [subjects.append(x) for x in SUBJECTS.get(n)]
    session['subject'] = subjects

    session['incomplete'] = [x for x in range(len(questions)) if check(questions[x], session.get('subject'), session.get('min_set'), session.get('min_round'), session.get('max_set'), session.get('max_round'))]
    
    to_json(session, 'session.json')

file_data = load_json('session.json')
attempted = file_data.get('attempted')
incomplete = file_data.get('incomplete')
score = file_data.get('score')
min_round = file_data.get('min_round')
max_round = file_data.get('max_round')
min_set = file_data.get('min_set')
max_set = file_data.get('max_set')
subjects = file_data.get('subject')


print('You currently are studying ' + ', '.join(x for x in subjects))
print('You are studying sets ' + str(min_set) + '-' + str(max_set) + ' and rounds ' + str(min_round) + '-' + str(max_round))
if attempted != 0:
    print('You have solved ' + str(score) + ' out of ' + str(attempted) + ' attempted questions')
print('There are ' + str(len(incomplete)) + ' questions left in this subject')
print()

while incomplete:
    
    # Select a question
    n = random.randint(0, len(incomplete) - 1)
    q = questions[incomplete[n]]
    incomplete.pop(n)

    # Print Question
    print('Set ' + q['set'] + ' Round ' + q['round'] + ' Question ' + q['number'])
    print()
    user = input(q['question'] + '\n')
    print()

    # Answer evaluation
    if SequenceMatcher(None, user.lower(), q['answer'].lower()).ratio() >= 0.8:
        print('Correct')
        result = 1

    else:
        print('Incorrect')
        result = 0
    
    user = input('The answer was ' + q['answer'] + ' (' + str(round(SequenceMatcher(None, user.lower(), q['answer'].lower()).ratio() * 100, 2)) + '%)\n')

    # Overrides
    if user.lower() == 'sub':
        result = 0
    elif user.lower() == 'add':
        result = 1
    elif user.lower() == 'null':
        result = 0
        attempted -= 1

    score += result
    attempted += 1

    if user.lower() == 'stop':
        to_json({
            'attempted' : attempted,
            'incomplete' : incomplete,
            'score' : score,
            'subject' : file_data.get('subject') 
            }, 'session.json')

        print('You saved your session.\nYou have solved ' + str(score) + ' out of ' + str(attempted) + ' questions')
        exit()
    
# Finish all questions
print('You have finished the set!\nYou solved ' + str(score) + ' out of ' + str(attempted) + ' questions')
