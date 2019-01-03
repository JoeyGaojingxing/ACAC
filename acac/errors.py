# _*_ coding: utf-8 _*_
"""
    :author: Mojerro (高景行)
    :url: http://mojerro.我爱你
    :copyright: © 2018
    :license: MIT, see LICENSE for more details
"""
from flask import render_template
from acac import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), e, 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), e, 500
