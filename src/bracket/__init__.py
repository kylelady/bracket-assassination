from flask import Flask
import os

#TODO: Convert all the JS build stuff to grunt and require

def _get_bracket_template_folder():
    folder = os.path.abspath(os.path.join(os.getcwd(), 'html'))
    return folder

def _get_bracket_static_folder():
    folder = os.path.abspath(os.path.join(os.getcwd(), 'static'))
    return folder

# Create the Flask object, with the correct template folder
app = Flask(__name__, 
        template_folder=_get_bracket_template_folder(),
        static_folder=_get_bracket_static_folder()
    )

# Set up routes
import routes