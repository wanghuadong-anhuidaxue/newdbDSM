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

@testblue.route('/testData', methods=['GET', 'POST'])
def testData():
    page = request.args.get('page',default=1,type=int)
    limit = request.args.get('limit', default=10,type=int)
    print(page, limit)
    pagination = AllData.query.filter(AllData.Disease.like('%1%')).paginate(page, limit, False)
    data = []
    for one_data in list(pagination.items):
        dict = {'dbid':'0', 'Disease':'1','Gene':'2','SNPID':'3','GRCh38_Position':'4','cDNA':'5','Protein':'6','dbDSMscore':'7','dbDSM_AccNum':'8'}
        dict['dbid'] = one_data.dbid
        dict['Disease'] = one_data.Disease
        dict['Gene'] = one_data.Gene
        dict['SNPID'] = one_data.SNPID
        dict['GRCh38_Position'] = one_data.Disease
        dict['cDNA'] = one_data.cDNA
        dict['Protein'] = one_data.Protein
        dict['dbDSMscore'] = one_data.DBDSMScore
        dict['dbDSM_AccNum'] = one_data.DBDSMID
        data.append(dict)
    # print(list(pagination.items)[0].Disease)
    jsondata = {
        "code": 0,
        "msg": "",
        "count": pagination.total,
        "data":data
    }
    return jsonify(jsondata)


@testblue.route('/test2', methods=['GET', 'POST'])
def test2():

    return render_template('temp.html')

@testblue.route('/limittest', methods=['GET', 'POST'])
def limittest():
    selectlimit = request.args.get('limit')
    return selectlimit