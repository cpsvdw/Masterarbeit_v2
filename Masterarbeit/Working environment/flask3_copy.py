import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'C:\\Users\\vanderweck\\PycharmProjects\\Masterarbeit\\Systemmodelle\\NewModel'
ALLOWED_EXTENSIONS = {'xmi'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('home.html')


@app.route('/commit_success')
def commit_success():
    return render_template('commit_success.html')


@app.route('/aufbau')
def aufbau():
    return render_template('aufbau.html')


# send data from this route to html
# to access we need jinja, special web syntax to access through html
@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('commit_success'))



if __name__ == '__main__':
    app.debug = True
    app.run()
