from flask import Flask
import os

def _get_bracket_template_folder():
    folder = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'html'))
    print folder
    return folder

# Create the Flask object, with the correct template folder
app = Flask(__name__, template_folder=_get_bracket_template_folder())

# Set up routes
import routes