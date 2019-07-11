from flask import Blueprint, Flask, Response, flash, redirect, render_template, request, session, abort, url_for
from flask import current_app as app

# set up Blueprint
home = Blueprint('home', __name__, url_prefix='/', template_folder='templates/')

@home.route('/', methods = ['GET','POST'])
def index():
    return render_template('home/index.html')
