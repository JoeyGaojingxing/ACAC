# _*_ coding: utf-8 _*_
"""
    :author: Mojerro (高景行)
    :url: http://
    :copyright: © 2018
    :license: MIT, see LICENSE for more details
"""
import os
import sys
import uuid

import click
import pandas as pd
from flask import Flask, flash, url_for, render_template, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone
# from flask_wtf.csrf import validate_csrf

from forms import SetTitleForm


# SQLite URI compatible
"""
兼容性设置
如果是Windows系统有3个'/'
Mac和Linux系统有2个'/'
"""
# by default, we use SQLite in development
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# if use mysql
# prefix = 'mysql://root:0327@localhost/test/'

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Custom config
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'demo.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Dropzone config
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image'
app.config['DROPZONE_MAX_FILE_SIZE'] = 3
app.config['DROPZONE_MAX_FILES'] = 30

# instantiate a db object of SQLAlchemy class
db = SQLAlchemy(app)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
        click.echo('Database dropped')
    db.create_all()
    click.echo('Initialized database')


dropzone = Dropzone(app)

# Forms


#Models
# TODO(Mojerro): add relationships and foreignkeys among tables.
class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean)
    id_num = db.Column(db.String(18))

    def __repr__(self):
        return '<User %r>' % self.name


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club = db.Column(db.String(15))
    logo_path = db.Column(db.String)

    def __repr__(self):
        return '<Club %r>' % self.club


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String)
    date = db.Column(db.Date)
    location = db.Column(db.String)

    def __repr__(self):
        return 'Game %r' % self.game


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename
    

@app.route('/game/name')
def game_name():
    form = SetTitleForm()
    return render_template('game_name.html', form=form)


# index page, use WTForm to upload excels.
@app.route('/', methods=['GET', 'POST'])
def index():
    # Excel files upload
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'This field is required.', 400
        f = request.files.get('file')

        if f and allowed_file(f.filename):
            filename = random_filename(f.filename)
            f.save(os.path.join(
                app.config['UPLOAD_PATH'], filename
            ))
        else:
            return 'Invalid file type.', 400
    return render_template('index.html')


# TODO(Mojerro): return the records(rows) which have problems,
# and save the rest records to database.
@app.route('/check')
def check():
    # try:
    #    df = load_regist_files()
    # except IOError:
    #     error = "error"
    # error_list = check_regist(df)
    return render_template('check.html')
 
 
@app.route('/download/gamecard')
def download_game_card():
     # TODO(Mojerro): search from the db and print to pics
     buildcard = game_card_builder()
     return render_template()
 

def load_regist_files():
    df = pd.DataFrame([1,2])
    return df


def check_regist(df):
    error_list = []
    return error_list


def game_card_builder(athelte, game, club, archer, date):

    return True

