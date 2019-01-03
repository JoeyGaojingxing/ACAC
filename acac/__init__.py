from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask('acac')
app.config.from_pyfile('settings.py')
# # the first newline after a block is removed
# app.jinja_env.trim_blocks = True
# # spaces and tabs are stripped from the start of a line to a block
# app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

from acac import views, errors, commands
