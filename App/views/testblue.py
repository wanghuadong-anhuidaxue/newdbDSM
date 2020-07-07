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



@testblue.route('/testData', methods=['GET', 'POST'])
def testData():

    return 'testData'