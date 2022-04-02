from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# db = SQLAlchemy(app)

# class Item(db.Model):

@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('home.html')


@app.route('/aufbau')
def aufbau():
    return render_template('aufbau.html')


# send data from this route to html
# to access we need jinja, special web syntax to access through html
@app.route('/upload')
def upload():
    item = [
        {'ID': 1, 'MAN': 'TGS', 'PRNummer': '893212299897', 'MaxWeight': '7-12'},
        {'ID': 2, 'MAN': 'TGM', 'PRNummer': '123985473165', 'MaxWeight': '13-26'},
        {'ID': 3, 'MAN': 'TGX', 'PRNummer': '231985128446', 'MaxWeight': '18-41'}
    ]
    return render_template('upload.html', items=item)


print ("This is a test for git")


if __name__ == '__main__':
    app.run()