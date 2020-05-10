#!/usr/bin/env python3

from datetime import datetime
from flask import Flask, render_template, request

empty_response = ('', 204)
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


# ifttt trigger logic
@app.route("/ifttt-trigger", methods=['GET', 'POST'])
def start_bus_watch():
    if request.content_length < 1e4:
        message = request.get_data(as_text=True)

    if message == "BUSWATCH":
        # import and immediately run busIndicator.py
        console_logger(message.lower())
        from scene_scripts import busIndicator
    elif message == "AURORA":
        # import and immediately run auroraBorealis.py
        console_logger(message.lower())
        from scene_scripts import auroraBorealis
    elif message == "STOP":
        # stop the running script

        return empty_response

def console_logger(module):
    print("Log {}: running {}".format(datetime.now(), module))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
