# _*_ coding: utf-8 _*_
"""
    :author: Mojerro (高景行)
    :url: http://mojerro.我爱你
    :copyright: © 2018
    :license: MIT, see LICENSE for more details
"""
from acac import db
from datetime import datetime


# Models
association_table = db.Table('association',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                             db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
                             )


class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)
    sex = db.Column(db.Boolean)
    archery = db.Column(db.String(32))
    id_num = db.Column(db.String(18), unique=True)  # ID card number
    remark = db.Column(db.Text(1024))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    club = db.relationship('Club')
    games = db.relationship('Game',
                            secondary=association_table,
                            back_populates='users')


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club = db.Column(db.String(32), unique=True)
    club_cut = db.Column(db.String(4), unique=True, index=True)
    logo_path = db.Column(db.String(127), unique=True)
    club_num = db.Column(db.Integer, unique=True, index=True)
    remark = db.Column(db.Text(1024))
    users = db.relationship('User')


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), unique=True)
    date = db.Column(db.Date, index=True)
    location = db.Column(db.String(127))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    remark = db.Column(db.Text(1024))
    users = db.relationship('User',
                            secondary=association_table,
                            back_populates='games')
