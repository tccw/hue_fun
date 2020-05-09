#!/usr/bin/env python3
from ..scene_scripts import busIndicator
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/ifttt", methods=['GET', 'POST']) 
def handler():
    busIndicator
    return "Huh"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=8080)
