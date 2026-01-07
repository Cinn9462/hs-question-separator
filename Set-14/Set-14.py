import os
import pdfplumber as pdf
import re
import json
import random
from difflib import SequenceMatcher

# Set working directory as file directory
PATH = os.path.realpath(__file__)
DIRECTORY = os.path.dirname(PATH)
os.chdir(DIRECTORY)

SET_NUMBER = "14"
SET = 'Set-14.json'
SUBJECTS = {
    "1" : ("MATH"),
    "2" : ("PHYSICS"),
    "3" : ("CHEMISTRY"),
    "4" : ("BIOLOGY"),
    "5" : ("EARTH SCIENCE", "ASTRONOMY", "EARTH AND SPACE")
}

NEW_GAME = {
    "attempted" : 0,
    "incomplete" : None,
    "score" : 0,
    "subject" : None
}

def extract(filename : str, round_number : str):
    
    with pdf.open(filename) as file:
        questions = [] # (set, round, question, subject, question, answer)
        lines = []

        for page in file.pages:

            text = page.extract_text()
            if text == None:
                continue

            
            lines += text.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Find question header
            m = re.match(r'(\d+)\)\s*(.*?)\s*–\s*(Multiple Choice|Short Answer)\s*(.*)', line)

            
            if m != None:
                number = m.group(1)[:-1]
                subject = m.group(2)
                qtext = m.group(4)

                # Get full question
                i += 1
                while (i < len(lines) and not re.match(r'ANSWER:|Answer:', lines[i])):
                    qtext += ' ' + lines[i].strip()
                    i += 1

                # Get answer
                answer = re.match(r'(ANSWER:|Answer:)\s*(.*)', lines[i])
                if answer.group(2)[0:2] in ['W)', 'X)', 'Y)', 'Z)']:
                    answer = answer.group(2)[0]
                else:
                    answer = answer.group(2).split('(')[0].strip()
                
                # Append to question list
                questions.append({
                    'set' : SET_NUMBER,
                    'round' : round_number,
                    'number' : number,
                    'subject' : subject,
                    'question' : qtext,
                    'answer' : answer
                    })

            i += 1
    
    return questions

def to_json(data, filename : str):
    with open(filename, 'w', encoding = 'utf-8') as f:
        json.dump(data, f, indent = 2)

def load_json(filename : str):
    with open(filename, 'r', encoding = 'utf-8') as f:
        return json.load(f)

def play():
    questions = load_json(SET)

    new = input("Would you like to start a new session [Y/N]\n")
    print()

    if new.lower() == 'y':
        session = NEW_GAME.copy()
        session['incomplete'] = list(range(len(questions)))
        session["subject"] = input("What subject would you like to play\n1) Math\n2) Physics\n3) Chemistry\n4) Biology\n5) Earth and space\n")
        print()
        
        to_json(session, "data.json")

    file_data = load_json('data.json')
    attempted = file_data.get("attempted")
    incomplete = file_data.get('incomplete')
    score = file_data.get('score')
    subject_number = file_data.get('subject')
    subject = SUBJECTS.get(subject_number)

    print("You currently are studying " + ", ".join(x for x in subject))
    print("You have solved " + str(score) + " out of " + str(attempted) + " questions")
    print()

    while incomplete:
        
        # Select a question
        n = random.randint(0, len(incomplete) - 1)
        q = questions[incomplete[n]]

        while (q['subject'].upper() not in subject):
            incomplete.pop(n)

            if not incomplete:
                print("You have finished the set!\nYou solved " + str(score) + " out of " + str(attempted) + " questions")
                exit()

            n = random.randint(0, len(incomplete) - 1)
            q = questions[incomplete[n]]

        incomplete.pop(n)

        # Print Question
        print("Set " + q['set'] + " Round " + q['round'] + " Question " + q['number'])
        print()
        user = input(q['question'] + "\n")
        print()

        # Answer evaluation
        if SequenceMatcher(None, user.lower(), q['answer'].lower()).ratio() >= 0.8:
            print("Correct")
            result = 1

        else:
            print("Incorrect")
            result = 0
        
        user = input("The answer was " + q['answer'] + ' (' + str(round(SequenceMatcher(None, user.lower(), q['answer'].lower()).ratio() * 100, 2)) + '%)\n')

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
                "attempted" : attempted,
                "incomplete" : incomplete,
                "score" : score,
                "subject" : subject_number
                }, "data.json")

            print("You saved your session.\nYou have solved " + str(score) + " out of " + str(attempted) + " questions")
            exit()
        


    # Finish all questions
    print("You have finished the set!\nYou solved " + str(score) + " out of " + str(attempted) + " questions")

# Convert pdf to json
questions = []
for n in range(7, 18):
    questions += extract('2019-NSB-HSR-Round-' + str(n) + 'A.pdf', str(n))

to_json(questions, SET)

# Check number of questions
questions = load_json(SET)
print(len(questions))

# Play
play()