# _*_ coding: utf-8 _*_
"""
    :author: Mojerro (高景行)
    :url: http://mojerro.我爱你
    :copyright: © 2018
    :license: MIT, see LICENSE for more details
"""
import sys
import os

from acac import app

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

# Custom config
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['DOWNLOAD_PATH'] = 'downloads'
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
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
