from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    logf = 'logs/events.log'
    logs = open(logf).read().splitlines() if os.path.exists(logf) else []
    imgs = sorted(os.listdir('assets/snapshots'), reverse=True)
    return render_template('index.html', logs=logs, images=imgs)

@app.route('/snapshots/<fn>')
def snap(fn):
    return send_from_directory('assets/snapshots', fn)