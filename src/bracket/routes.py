from . import app
from flask import render_template, request

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.view')

@app.route('/bracket')
def bracket():
	return render_template('bracket.view')




