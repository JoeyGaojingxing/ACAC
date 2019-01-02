# _*_ coding: utf-8 _*_
"""
    :author: Mojerro (高景行)
    :url: http://
    :copyright: © 2018
    :license: MIT, see LICENSE for more details
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


# set game title
class SetTitleForm(FlaskForm):
    name = StringField('输入ACAC比赛名称', validators=[DataRequired(), Length(-1, 31)])
    date = StringField('输入比赛日期 如：2018-3-9', validators=[Length(-1, 10)])    # TODO: 优化日期输入验证
    location = StringField('输入比赛地点', validators=[Length(-1, 127)])
    submit = SubmitField('提交')
