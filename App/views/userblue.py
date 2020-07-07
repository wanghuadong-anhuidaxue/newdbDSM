from flask import Blueprint, render_template, request, session, redirect, url_for

from App.models import db, User

userblue = Blueprint("userblue", __name__)


@userblue.route('/', methods=['post', 'get'])
def logindex():
    username = session.get('username')
    password = session.get('password')

    if username is not None:
        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            if username == db_user.username and password == db_user.password:
                print(db_user.username+db_user.password)
                return redirect(url_for('bioblue.bioindex'))
        else:
            print('怎么可能')
    return redirect(url_for('userblue.login'))


@userblue.route('/login', methods=['post', 'get'])
def login():
    return render_template('login.html')


@userblue.route('/userSubmit', methods=['post', 'get'])
def userSubmit():
    username = request.form.get('username')
    password = request.form.get('password')

    session.permanent = True  # 默认session的时间持续31天
    session['username'] = username
    session['password'] = password

    db_user = User.query.filter_by(username=username).first()
    if db_user is not None:
        if username == db_user.username and password == db_user.password:
            return redirect(url_for('bioblue.bioindex')) #跨py文件重定向
        else:
            session.pop('username')
            session.pop('password')
            return "password ERROR"
    else:
        session.pop('username')
        session.pop('password')
        return "username ERROR"


@userblue.route('/upgradeUser')
def upgradeUser():
    return render_template('upgrade_user.html')


@userblue.route('/upgradeUserSubmit', methods=['post', 'get'])
def upgradeUserSubmit():
    username = session.get('username')
    newpassword = request.form.get('newpassword')
    db_user = User.query.filter_by(username=username).first()
    db_user.password = newpassword
    db.session.commit()
    session.pop('username')
    session.pop('password')
    return redirect(url_for('userblue.login'))


