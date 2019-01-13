# _*_ coding: utf-8 _*_
"""
    :author: Mojerro (高景行)
    :url: http://mojerro.我爱你
    :copyright: © 2018
    :license: MIT, see LICENSE for more details
"""
from acac.utils import *
from acac.forms import SetTitleForm, SubmitForm
from datetime import datetime
from flask import flash, url_for, render_template, request, redirect, make_response, send_from_directory, send_file
# from threading import Thread


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


@app.route('/set/<int:game_id>')
def set_cookie(game_id):
    if game_id:
        response = make_response(redirect(url_for('game_upload')))
        response.set_cookie('game_id', str(game_id))
        make_dirs(os.path.join(app.config['UPLOAD_PATH'], str(game_id)))
    else:
        raise NameError
    return response


# use WTForm to upload excels.
@app.route('/game/upload/', methods=['GET', 'POST'])
def game_upload():
    # Excel files upload
    game_id = request.cookies.get('game_id')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'This field is required.', 400
        f = request.files.get('file')

        if f and allowed_file(f.filename):
            filename = random_filename(f.filename, game_id=game_id)
            f.save(os.path.join(
                app.config['UPLOAD_PATH'], game_id, filename
            ))
        else:
            return 'Invalid file type.', 400
    return render_template('game_upload.html')


# return the records(rows) which have problems and save the rest records to database.
@app.route('/game/check/')
def check():
    game_id = request.cookies.get('game_id')  # game_id is a string
    '''
        俱乐部       	        姓名 	性别 弓种 	Unnamed: 4
    0 	深圳聚贤庄射箭俱乐部  	陈豪 	男 	反曲50M NaN
    1 	深圳聚贤庄射箭俱乐部 	    魏亮 	男 	反曲弓 	NaN
    2 	唐山鸿鹄射箭运动俱乐部 	候雨辰 	男 	反曲弓 	NaN
    3 	唐山鸿鹄射箭运动俱乐部 	刘崎 	男 	反曲弓 	NaN
    4 	唐山鸿鹄射箭运动俱乐部 	马天宇 	男 	反曲弓 	NaN
    5 	唐山鸿鹄射箭运动俱乐部 	李清语 	女 	反曲弓 	NaN
    6 	唐山鸿鹄射箭运动俱乐部 	胡洋 	男 	复合弓 	NaN
    7 	北京大学射箭代表队 	    林达 	男 	反曲弓 	NaN
    '''
    # choose the file
    val_list, error_list = check_regist(game_id)
    flash('导入成功')
    return render_template('check.html', error_list=error_list)  # 错误输出到网页，格式优化


# TODO(Mojerro): return download link, 实现页面等待效果
@app.route('/download/gamecard', methods=['GET', 'POST'])
def download_game_card():
    game_id = request.cookies.get('game_id')  # game_id is a string
    # search from the db and print to pics
    form = SubmitForm()
    if form.download.data:
        builder = GameCardBuilder(game_id, './acac/static/images/gamecard/2019.png')
        card_dir = builder.render()
        return send_file(card_dir, as_attachment=True, attachment_filename='demo.zip')
    return render_template('game_download.html', form=form)
