import os,errno
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, send_file,session, jsonify
from flask_bootstrap import Bootstrap
import requests
import sys
import json

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
bootstrap = Bootstrap(app)

@app.route('/')
def landingPage():
    return "You are at Scheduler module"

if __name__ == '__main__':

    app.run(host="0.0.0.0",debug=True,port=8000,threaded=True)
