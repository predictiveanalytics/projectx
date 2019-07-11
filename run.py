from flask import Flask, Response, flash, redirect, render_template, request, session, abort, url_for
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.config.from_object('config')
cors = CORS(app)

# CORS settings
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# import blueprints
from home.views import home
app.register_blueprint(home)

from classifier.views import classifier
app.register_blueprint(classifier)

from emails.views import emails
app.register_blueprint(emails)




if __name__ == "__main__":
    with app.app_context():
        app.run(host='0.0.0.0')
