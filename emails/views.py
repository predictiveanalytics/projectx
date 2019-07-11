from flask import Blueprint, Flask, Response, flash, redirect, render_template, request, session, abort, url_for
from flask import current_app as app
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
from urllib import unquote

from functions.emails import *

# module configuration
ALLOWED_EXTENSIONS = set(['csv'])

# verify that file has proper extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# set up Blueprint
emails = Blueprint('emails', __name__, url_prefix='/emails', template_folder='templates/')

@emails.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        # check for invalid requests
        if ('file' not in request.files):
            flash('No file part')
            return redirect(request.url)
        input_file = request.files['file']

        # verify proper formatting
        if (input_file.filename == ''):
            flash('No selected file')
            return redirect(request.url)

        # if request is good, process file
        if (input_file and allowed_file(input_file.filename)):
            input_filename = secure_filename(input_file.filename)
            input_file.save(os.path.join(app.config['UPLOAD_FOLDER'], input_filename))

            return redirect(unquote(url_for('emails.configure', input_filename=input_filename)))


    return render_template('emails/index.html', ready=False)

@emails.route("/configure/input=<input_filename>", methods=['GET', 'POST', 'OPTIONS'])
def configure(input_filename):
    
    input_filepath = "data/" + input_filename

    if request.method == 'POST':
        email_col = request.form['input_col']

        return redirect(unquote(url_for('emails.process', input_file=input_filename, email_col=email_col)))


    input_cols = read_csv(input_filepath)

    return render_template('emails/configure.html', input_cols=input_cols)


@emails.route("/process/file=<input_file>&col=<email_col>", methods=['GET', 'POST', 'OPTIONS'])
def process(input_file, email_col):

    input_filepath = "data/" + input_file

    if (request.method =='POST'):
        val = process_file(input_filepath, email_col)

        if val:
            return send_from_directory(app.config['UPLOAD_FOLDER'], "output.csv", as_attachment=True)
        else:
            flash('did not work')

    return render_template('emails/process.html')