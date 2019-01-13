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
import zipfile
import datetime

from acac import app, db
from acac.models import Club, User, Game
from sqlalchemy.exc import IntegrityError
from PIL import Image, ImageDraw, ImageFont


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
    elif '传统' in name:
        return '传统'
    elif '光弓' in name:
        return '光弓'
    else:
        raise TypeError


def judge_sex(sex):
    if '男' in sex:
        return 1
    elif '女' in sex:
        return 0
    else:
        raise NameError


class GameCardBuilder(object):

    def __init__(self, game_id, template):
        self.id = game_id
        self.template = template
        self.download = os.path.join(os.getcwd(), app.config['DOWNLOAD_PATH'])
        self.path = os.path.join(self.download, game_id)

    def _query_from_db(self):
        sql = "SELECT `user`.`name`,`user`.sex,`user`.archery, club.club_num, `user`.id_num, game.`name` \
                FROM game \
                INNER JOIN association ON `game`.id = association.game_id \
                INNER JOIN `user` ON association.user_id = `user`.id \
                INNER JOIN club ON club.id = `user`.club_id \
                WHERE game_id={}".format(self.id)
        self.query = db.session.execute(sql)
        return self.query

    def render(self):
        lists = self._query_from_db().fetchall()
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        for info in lists:
            rc = self.render_card(info)
            if not rc:
                raise IOError
        return self.zip_dir(os.path.join(self.path), os.path.join(self.download,
                            '{}.zip'.format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))))

    def render_card(self, info):

        # TODO(mojerro): 实现生成并存储参赛证图片
        # 打开模板图像
        img = Image.open(os.path.join(os.getcwd(), 'acac/static/images/gamecard/2019.png'))
        # 创建Font对象:
        font_path = os.path.join(os.getcwd(), 'acac/static/fonts/msyh.ttf')
        font = ImageFont.truetype(font_path, 36)  # TODO：注意修改字体路径
        # 创建Draw对象:
        draw = ImageDraw.Draw(img)
        # pname = self.name % num

        # 输出文字:0姓名name，1性别sex，2运动员号ID，3弓种archery，4俱乐部club_num，5game_name
        draw.text((20, 10), info[0], font=font, fill='Black')

        if info[1]:
            psex = Image.open(os.path.join(os.getcwd(), 'acac/static/images/sex/boy.jpg'))
        else:
            psex = Image.open(os.path.join(os.getcwd(), 'acac/static/images/sex/girl.jpg'))
        img.paste(psex, (20, 10))

        draw.text((20, 10), info[2], font=font, fill='Black')
        # img.paste(pclub, (20, 10))
        # draw.text((20, 10), group, font=font, fill='Black')
        # draw.text((20, 10), author, font=font, fill='Black')
        img.save(os.path.join(self.path, '{}.png'.format(info[0])))
        return True

    @staticmethod
    def zip_dir(dirpath, outfullname):
        """
        压缩指定文件夹
        :param dirpath: 目标文件夹路径
        :param outfullname: 压缩文件保存路径+xxxx.zip
        :return: 无
        """
        zip = zipfile.ZipFile(outfullname, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(dirpath):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(dirpath, '')

            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()
        return outfullname


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
