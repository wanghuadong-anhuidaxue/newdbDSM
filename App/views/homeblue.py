
from flask import Blueprint, render_template, session, escape, redirect, url_for, request

from App.models import db, AllData

homeblue = Blueprint("homeblue",__name__)


@homeblue.route('/searchresult')
@homeblue.route('/newdbDSM/searchresult')
def searchresult():
    return render_template("searchresult.html")




@homeblue.route('/')
@homeblue.route('/newdbDSM/')
def index():
    return render_template("index.html")


@homeblue.route('/home')
@homeblue.route('/newdbDSM/home')
def hello():
    return render_template("nav_temp.html")






@homeblue.route('/download')
@homeblue.route('/newdbDSM/download')
def download():
    return render_template("download.html")


@homeblue.route('/about')
@homeblue.route('/newdbDSM/about')
def about():
    return render_template("about.html")



@homeblue.route('/contact')
@homeblue.route('/newdbDSM/contact')
def contact():
    return render_template("contact.html")
