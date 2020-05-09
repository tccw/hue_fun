#!/usr/bin/env python3

from flask import Flask, render_template, request

empty_response = ('', 204)
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

# Bus route watcher 
@app.route("/buswatch", methods=['GET', 'POST']) 
def start_bus_watch():
    # import and immediately run busIndicator
    from scene_scripts import busIndicator
    return "Huh"

@app.route("/stopbuswatch", methods=['GET', 'POST'])
def stop_bus_watch():
    # do something to stop the busIndicator script
    return empty_response

# Aurora borealis lights
@app.route("/aurora", methods=['GET','POST'])
def start_aurora():
    from scene_scripts import auroraBorealis
    return empty_response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=8080)
