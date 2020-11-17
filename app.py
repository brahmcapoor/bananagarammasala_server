from flask import Flask, jsonify
from flask_cors import CORS

from collections import Counter

import csv
import os
import string
import random

app = Flask(__name__)
CORS(app)

CLUES_DIRECTORY = 'clues' 


def get_data_from_clues(filename):
    data = []
    filename = os.path.join(CLUES_DIRECTORY, filename)
    with open(filename) as f:
        details = next(f)
        reader = csv.reader(f)
        for line in reader:
            data.append({'clue': line[0].strip(), 'answer': line[1].strip().upper()})

    random.shuffle(data)
    
    return details, data

@app.route('/<clueset>')
def get_clueset(clueset):
    details, clue_data = get_data_from_clues(f'{clueset}.txt')
    letter_counts = get_letter_counts(clue_data)
    return jsonify(
        details=details,
        clues=clue_data
    )

@app.route('/cluesets')
def get_all_cluesets():
    return jsonify(cluesets = [f[:-4] for f in os.listdir(CLUES_DIRECTORY) if f.endswith('.txt')] )