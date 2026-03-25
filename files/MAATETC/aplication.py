from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    '''Index page route'''
    return render_template('index.html')

@app.route('/doc')
def doc():
    return render_template('doc.html')