from flask import Blueprint, render_template

from App.models import db, User

blue = Blueprint("blue", __name__)


@blue.route('/')
def index():
    return render_template("index.html")


@blue.route('/main')
def main():
    return render_template("main.html")


@blue.route('/createdb/')
def createdb():
    db.create_all()
    return "成功！"


@blue.route('/adduser/')
def adduser():
    user = User()
    user.username = "Tom"
    db.session.add(user)
    db.session.commit()
    return "users创建成功！"
