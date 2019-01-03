# _*_ coding: utf-8 _*_
"""
    :author: Mojerro (高景行)
    :url: http://
    :copyright: © 2018
    :license: MIT, see LICENSE for more details
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length


# set game title
class SetTitleForm(FlaskForm):
    name = StringField('输入ACAC比赛名称', validators=[DataRequired(), Length(-1, 31)])
    date = DateField('输入比赛日期 如：2018-3-9', validators=[DataRequired()])
    location = StringField('输入比赛地点', validators=[Length(-1, 127)])
    submit = SubmitField('提交')


class SubmitForm(FlaskForm):
    execute = SubmitField('执行')
    download = SubmitField('下载')
