from flask import Blueprint, Flask, Response, flash, redirect, render_template, request, session, abort, url_for
from flask import current_app as app
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
from urllib import unquote

from functions.classifier import *


# module configuration
ALLOWED_EXTENSIONS = set(['csv'])

# set up Blueprint
classifier = Blueprint('classifier', __name__, url_prefix='/classifier', template_folder='templates/')

# verify that file has proper extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@classifier.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        # check for invalid requests
        if ('train_file' not in request.files) or ('eval_file' not in request.files):
            flash('No file part')
            return redirect(request.url)
        train_file = request.files['train_file']
        eval_file = request.files['eval_file']

        # verify proper formatting
        if (train_file.filename == '') or (eval_file.filename == ''):
            flash('No selected file')
            return redirect(request.url)

        # if request is good, process file
        if (train_file and allowed_file(train_file.filename)) and (eval_file and allowed_file(eval_file.filename)) :
            train_filename = secure_filename(train_file.filename)
            train_file.save(os.path.join(app.config['UPLOAD_FOLDER'], train_filename))

            eval_filename = secure_filename(eval_file.filename)
            eval_file.save(os.path.join(app.config['UPLOAD_FOLDER'], eval_filename))

            return redirect(unquote(url_for('classifier.configure', train_filename=train_filename, eval_filename=eval_filename)))


    return render_template('classifier/index.html', ready=False)


@classifier.route("/configure/train=<train_filename>&eval=<eval_filename>", methods=['GET', 'POST', 'OPTIONS'])
def configure(train_filename, eval_filename):
    
    train_filepath = "data/" + train_filename
    eval_filepath = "data/" + eval_filename

    if request.method == 'POST':
        train_input = request.form['train_input']
        train_classes = request.form['train_classes']
        eval_input = request.form['eval_input']

        return redirect(unquote(url_for('classifier.process', train_filename=train_filename, eval_filename=eval_filename, train_input=train_input, train_classes=train_classes, eval_input=eval_input)))


    train_cols = read_csv(train_filepath)
    eval_cols = read_csv(eval_filepath)

    return render_template('classifier/configure.html', train_cols=train_cols, eval_cols=eval_cols)

@classifier.route("/process/train_input=<train_input>&train_classes=<train_classes>&eval_input=<eval_input>&train_filename=<train_filename>&eval_filename=<eval_filename>", methods=['GET', 'POST', 'OPTIONS'])
def process(train_input, train_classes, eval_input, train_filename, eval_filename):

    train_filepath = "data/" + train_filename
    eval_filepath = "data/" + eval_filename


    if (request.method =='POST'):
        val = train_model(train_input, train_classes, eval_input, train_filepath, eval_filepath)

        if val:
            return send_from_directory(app.config['UPLOAD_FOLDER'], "output.csv", as_attachment=True)
        else:
            flash('did not work')

    return render_template('classifier/process.html')