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
from datetime import datetime
from flask import Flask, flash, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone
from flask_moment import Moment
from flask_bootstrap import Bootstrap
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
mysql_prefix = 'mysql+pymysql://root:'

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Custom config
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['SECRET_KEY'] = mysql_prefix + os.getenv('SECRET_KEY', 'secret string')
app.config['ALLOWED_EXTENSIONS'] = ['xls', 'xlsx']

# SQLAlchemy config
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'demo.sqlite'))
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_prefix + os.getenv('MYSQL_PASS', '0327') + '@' \
                                        + os.getenv('MYSQL_URI', 'localhost') + '/acac_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Dropzone config
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.xls, .xlsx'
app.config['DROPZONE_MAX_FILE_SIZE'] = 3
app.config['DROPZONE_MAX_FILES'] = 30
# app.config['DROPZONE_ENABLE_CSRF'] = True

# instantiate a db object of SQLAlchemy class
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
dropzone = Dropzone(app)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
        click.echo('Database dropped')
    db.create_all()
    click.echo('Initialized database')


# Forms


# Models
association_table = db.Table('association',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                             db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
                             )


class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)
    sex = db.Column(db.Boolean)
    id_num = db.Column(db.String(18), unique=True)  # ID card number
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    club = db.relationship('Club')
    games = db.relationship('Game',
                            secondary=association_table,
                            back_populates='users')

    # def __repr__(self):
    #     return '<User %r>' % self.name


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club = db.Column(db.String(16), unique=True)
    logo_path = db.Column(db.String(127), unique=True)
    club_num = db.Column(db.Integer, unique=True, index=True)
    users = db.relationship('User')

    # def __repr__(self):
    #     return '<Club %r>' % self.club


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), unique=True)
    date = db.Column(db.Date, index=True)
    location = db.Column(db.String(127))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    users = db.relationship('User',
                            secondary=association_table,
                            back_populates='games')

    # def __repr__(self):
    #     return 'Game %r' % self.game


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def random_filename(filename, game_id: str):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return str(game_id) + '_' + new_filename


# index page, set game name
@app.route('/', methods=['GET', 'POST'])
@app.route('/game/name', methods=['GET', 'POST'])
def game_name():
    # register game name
    games = Game.query.order_by(Game.timestamp.desc()).all()
    form = SetTitleForm()
    if form.validate_on_submit():
        name = form.name.data
        date = default(form.date.data, datetime.now())
        location = default(form.location.data, '默认')
        add_game = Game(name=name, date=date, location=location)
        db.session.add(add_game)
        db.session.commit()
        flash('提交成功')
        return redirect(url_for('game_name'))
    return render_template('game_name.html', form=form, games=games)


# use WTForm to upload excels.
@app.route('/game/upload/<int:game_id>', methods=['GET', 'POST'])
# @app.route('/game/upload', methods=['GET', 'POST'])
def game_upload(game_id=None):
    # Excel files upload
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'This field is required.', 400
        f = request.files.get('file')

        if f and allowed_file(f.filename):
            filename = random_filename(f.filename, game_id=game_id)
            f.save(os.path.join(
                app.config['UPLOAD_PATH'], filename
            ))
        else:
            return 'Invalid file type.', 400
    return render_template('game_upload.html', game_id=game_id)


# TODO(Mojerro): return the records(rows) which have problems
# and save the rest records to database.
@app.route('/game/check')
def check():
    # try:
    #    df = load_regist_files()
    # except IOError:
    #     error = "error"
    # error_list = check_regist(df)
    return render_template('check.html')
 

# TODO(Mojerro): return download link
@app.route('/download/gamecard')
def download_game_card():
    # TODO(Mojerro): search from the db and print to pics
    buildcard = game_card_builder()
    return render_template('game_download.html')
 

def default(value, default):
    if value:
        return value
    return default


def load_regist_files():
    df = pd.DataFrame([1, 2])
    return df


def check_regist(df):
    error_list = []
    return error_list


def game_card_builder(athelte, game, club, archer, date):

    return True

