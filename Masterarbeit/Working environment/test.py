from flask import Flask, render_template, request, url_for

from werkzeug.utils import secure_filename, redirect

app = Flask(__name__)


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
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        #uploaded_file.save(os.path.join(app.config['Masterarbeit/Systemmodelle/NewModel']))
    return redirect(url_for('commit_success'))

if __name__ == '__main__':
    app.debug = True
    app.run()
