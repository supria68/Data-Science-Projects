"""
filename: app.py
author: Supriya Sudarshan
version: 12.11.2020

description: This script consists of functions to deploy the Plagiarism checker
using Flask
"""

from flask import Flask, render_template, request
import helper

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])

def result():
    if request.method == 'POST':
        text = request.form['text']
        with open('database.txt', 'w') as f:
            f.write('')
        match_sites, match_percent = helper.queryWeb(text)
        return render_template('index.html', out = 'Match percentage: {} %'.format(round(match_percent, 2)), out2 = 'Source urls : {}'.format(match_sites))

if __name__ == '__main__':
    app.run(debug = True)
