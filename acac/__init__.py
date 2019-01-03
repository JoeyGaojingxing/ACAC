# _*_ coding: utf-8 _*_
"""
    :author: Mojerro (高景行)
    :url: http://mojerro.我爱你
    :copyright: © 2018
    :license: MIT, see LICENSE for more details
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone
from werkzeug.contrib.fixers import ProxyFix

app = Flask('acac')
app.config.from_pyfile('settings.py')
# the first newline after a block is removed
app.jinja_env.trim_blocks = True
# spaces and tabs are stripped from the start of a line to a block
app.jinja_env.lstrip_blocks = True
app.wsgi_app = ProxyFix(app.wsgi_app)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
dropzone = Dropzone(app)

from acac import views, errors, commands
