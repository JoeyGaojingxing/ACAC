# _*_ coding: utf-8 _*_
"""
    :author: Mojerro (高景行)
    :url: http://mojerro.我爱你
    :copyright: © 2018
    :license: MIT, see LICENSE for more details
"""
import os
import uuid
import pandas as pd

from acac import app, db
from acac.models import Club, User, Game
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import BaseQuery


def default(value, defaults):
    if value:
        return value
    return defaults


def load_regist_files():
    df = pd.DataFrame([1, 2])
    return df


# insert contents into DataBase
def check_regist(game_id):
    vali_list = []
    error_list = []
    game = Game.query.filter_by(id=game_id).first()
    path = os.path.join(app.config['UPLOAD_PATH'], game_id)
    for file in os.listdir(path):
        df = pd.read_excel(os.path.join(path, file))
        clubs = df.iloc[:, 0]
        length = len(clubs)
        for i in range(length):
            club = Club.query.filter_by(club=clubs[i]).first()
            if club:
                info = df.loc[i, ['姓名', '性别', '弓种']].append(pd.Series({'club_id': club.id}))
                vali_list.append(info)
                try:
                    user = User.query.filter_by(name=info.loc['姓名']).first()
                    if user and user.sex == judge_sex(info.loc['性别']):
                        user.archery = judge_archery_type(info.loc['弓种'])
                    else:
                        user = User(name=info.loc['姓名'],
                                    sex=judge_sex(info.loc['性别']),
                                    archery=judge_archery_type(info.loc['弓种']),
                                    club_id=info.loc['club_id'])
                    game.users.append(user)
                    db.session.add(user)
                except NameError:
                    error_list.append(df.iloc[i].append(pd.Series({'备注': '性别填写有误'})))
                except TypeError:
                    error_list.append(df.iloc[i].append(pd.Series({'备注': '弓种组别填写有误'})))
            else:
                error_list.append(df.iloc[i].append(pd.Series({'备注': '俱乐部未查到'})))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return vali_list, error_list


# TODO(Mojerro): add group judge, 复合 反曲 光弓 传统
def judge_archery_type(name):
    if '反曲' in name:
        return '复合'
    elif '复合' in name:
        return '反曲'
    else:
        raise TypeError


def judge_sex(sex):
    if '男' in sex:
        return 1
    elif '女' in sex:
        return 0
    else:
        raise NameError


def game_card_builder(athelte, game, club, archer, date):
    link = os.path.join()
    return link


def make_dirs(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    exists = os.path.exists(path)
    if not exists:
        os.makedirs(path)
        return True
    else:
        return False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def random_filename(filename, game_id: str):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return game_id + '_' + new_filename
