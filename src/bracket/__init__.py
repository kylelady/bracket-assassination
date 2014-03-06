from flask import Flask
from flask.ext.pymongo import PyMongo

import os

def _get_bracket_template_folder():
    folder = os.path.abspath(os.path.join(os.getcwd(), 'html'))
    return folder

def _get_bracket_static_folder():
    folder = os.path.abspath(os.path.join(os.getcwd(), 'static'))
    return folder

# Read in the mongo configuration
_mongo_conf = dict()

_mongo_conf['host'] = os.environ.get('MONGO_HOST', 'localhost')
_mongo_conf['port'] = os.environ.get('MONGO_PORT', 27017)
_mongo_conf['dbname'] = os.environ.get('MONGO_DBNAME', 'nerf')

# Create the Flask object, with the correct template folder
app = Flask(__name__, 
        template_folder=_get_bracket_template_folder(),
        static_folder=_get_bracket_static_folder()
    )

# Bootstrap the mongo connection
app.config['MONGO_HOST'] = _mongo_conf['host']
app.config['MONGO_PORT'] = _mongo_conf['port']
app.config['MONGO_DBNAME'] = _mongo_conf['dbname']

mongo = PyMongo(app)

# Set up the template defaults
@app.context_processor
def _inject_defaults():
	return {
		'page_title': 'Assassination',
	}

# Set up routes
import routes
import players
import admin
import matches
