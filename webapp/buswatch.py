#!/usr/bin/env python3
# External listening port 9847
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/ifttt", methods=['GET', 'POST']) 
def handler():
    print("Wow Heather! You are so mgical and lovely!")
    return "There is nothing here right now"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=8080)
