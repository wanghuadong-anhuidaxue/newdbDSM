from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from App.models import db, AllData
from sqlalchemy import or_,and_
import json
testblue = Blueprint("testblue", __name__)



@testblue.route('/test', methods=['GET', 'POST'])
def test():
    '''
    测试
    :return:
    '''
    return render_template('test.html')

@testblue.route('/testdemo', methods=['GET', 'POST'])
def testdemo():

    return render_template('testdemo.html')

@testblue.route('/testAction', methods=['GET', 'POST'])
def testAction():

    return render_template('testdemo.html',)



@testblue.route('/test2', methods=['GET', 'POST'])
def test2():

    return render_template('temp.html')

@testblue.route('/limittest', methods=['GET', 'POST'])
def limittest():
    selectlimit = request.args.get('limit')
    return selectlimit