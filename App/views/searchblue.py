from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .forms import SearchForm#,AdvancedSearchForm #导入本地写的forms.py
from App.models import db, AllData
from sqlalchemy import or_,and_
import json
searchblue = Blueprint("searchblue", __name__)




@searchblue.route('/search')
@searchblue.route('/newdbDSM/search', methods=['GET', 'POST'])
def search():
    '''
    跳转到查询表单，wtf负责第一个search表单，第二个高级搜索使用原始的方式，因为wtf如何实现ajax实时更新我不会。
    :return:
    '''
    form = SearchForm()
    form.searchBy.data = 'Disease'#默认选择，不然就是中文的请选择了
    return render_template("search.html", form=form)


def showTable(indata, page, limit):
    '''
    为普通搜索进行sql查询，分页
    :param indata: searchBy，和userinput
    :param page: 当前页
    :param limit: 每页个数
    :return: 返回查询分页结果
    '''
    searchBy = indata[0]
    userinput = indata[1]
    if searchBy == 'Disease':
        paginate = AllData.query.filter(AllData.Disease.like('%'+userinput+'%')).paginate(page, limit, False)
    elif searchBy == 'Gene':
        paginate = AllData.query.filter(AllData.Gene.like('%'+userinput+'%')).paginate(page, limit, False)
    elif searchBy == 'GRCh38_Position':
        paginate = AllData.query.filter(AllData.GRCh38_Position.like('%'+userinput+'%')).paginate(page, limit, False)
    elif searchBy == 'Mutation':
        paginate = AllData.query.filter(or_(AllData.Protein.like('%'+userinput+'%'),
                                           AllData.cDNA.like('%'+userinput+'%'),
                                           AllData.SNPID.like('%'+userinput+'%'))).paginate(page, limit, False)
    elif searchBy == 'DBDSMScore':
        paginate = AllData.query.filter(AllData.DBDSMScore.like('%'+userinput+'%')).paginate(page, limit, False)
    else:
        paginate = []
    return paginate

@searchblue.route('/searchSubmit', methods=['GET', 'POST'])
def searchSubmit():
    '''
    普通查询首次提交
    :return: 使用的是request.form调用
    '''
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    searchBy = request.form.get("searchBy")
    userinput = request.form.get("userinput")
    paginate = showTable((searchBy, userinput), page, per_page)
    return render_template('searchresult.html', searchBy=searchBy, userinput=userinput, pagination=paginate, search_result=searchBy+' like:'+userinput)

@searchblue.route('/searchTable', methods=['GET', 'POST'])
def searchTable():
    '''
    表单更新
    :return:使用的是request.args调用
    '''
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    searchBy = request.args.get("searchBy")
    userinput = request.args.get("userinput")
    paginate = showTable((searchBy, userinput), page, per_page)
    return render_template('searchresult.html',page=page,per_page=per_page, searchBy=searchBy, userinput=userinput, pagination=paginate, search_result=searchBy+' like:'+userinput)



@searchblue.route('/detailScore', methods=['GET', 'POST'])
def detailScore():
    dbid = request.args.get("dbid")
    result = AllData.query.filter_by(dbid=dbid).first()
    return render_template('details.html',dbDSMData = result)


@searchblue.route('/advancedSearch', methods=['GET'])
def advancedSearch():
    Disease = request.args.get('Disease')
    Gene = request.args.get('Gene')
    Chromosome = request.args.get('Chromosome')
    DBDSMScore = request.args.get('DBDSMScore')
    flags = {'Disease':1, 'Gene':1, 'Chromosome':1, 'DBDSMScore':1}#立标签
    sql = 'select dbid,DBDSMID'\
          +(",Disease" if(Disease=="" or Disease==None) else"")\
          +(",Gene" if (Gene == "" or Gene == None) else "")\
          +(",Chromosome" if (Chromosome == "" or Chromosome == None) else "")\
          +(",DBDSMScore" if (DBDSMScore == "" or DBDSMScore == None) else "")\
          + " from all_data where DBDSMID like '%'"\
          +("" if(Disease=="" or Disease==None) else(" and Disease='%s'"%Disease))\
          +("" if (Gene == "" or Gene == None) else (" and Gene='%s'"%Gene)) \
          + ("" if (Chromosome == "" or Chromosome == None) else (" and Chromosome='%s'"%Chromosome)) \
          + ("" if (DBDSMScore == "" or DBDSMScore == None) else (" and DBDSMScore='%s'"%DBDSMScore)) +';'
    # print('sql:',sql)
    result = db.session.execute(sql)
    if (Disease == "" or Disease == None):
        flags['Disease'] = 0
    if (Gene == "" or Gene == None):
        flags['Gene'] = 0
    if (Chromosome == "" or Chromosome == None):
        flags['Chromosome'] = 0
    if (DBDSMScore == "" or DBDSMScore == None):
        flags['DBDSMScore'] = 0

    payload = result_to_dict(result,flags)#转为字典
    return jsonify(payload)


@searchblue.route('/advancedSearchTable', methods=['GET'])
def advancedSearchTable():
    '''
    表单更新
    :return:
    '''
    Disease = request.args.get('Disease')
    Gene = request.args.get('Gene')
    Chromosome = request.args.get('Chromosome')
    DBDSMScore = request.args.get('DBDSMScore')
    dict = {
        'Disease': Disease
        , 'Gene': Gene
        , 'Chromosome': Chromosome
        , 'DBDSMScore': DBDSMScore
            }
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    # print('dict',dict)
    paginate = showAdvancedTable(dict, page, per_page)
    return render_template('searchresult2.html',page=page,per_page=per_page, pagination=paginate, Disease=Disease, Gene=Gene, Chromosome=Chromosome, DBDSMScore=DBDSMScore)

def showAdvancedTable(dict, page, limit):
    '''
    高级搜索，sql查询
    :param dict:
    :param page:
    :param limit:
    :return:
    '''
    Disease = dict['Disease']
    Gene = dict['Gene']
    Chromosome = dict['Chromosome']
    DBDSMScore = dict['DBDSMScore']
    return AllData.query.filter(and_(AllData.Gene.like('%'+"" if(Gene=="" or Gene==None) else Gene+'%'),
                                        AllData.Disease.like('%'+"" if(Disease=="" or Disease==None) else Disease+'%'),
                                        AllData.Chromosome.like('%'+"" if(Chromosome=="" or Chromosome==None) else Chromosome+'%'),
                                        AllData.DBDSMScore.like('%'+"" if(DBDSMScore=="" or DBDSMScore==None) else DBDSMScore+'%'))).paginate(page, limit, False)



def result_to_dict(result,flags):
    '''
    把sql结果转换为对应的字典，方便json传输
    :param result:
    :param flags:
    :return:
    '''
    import numpy as np
    # print(flags)
    dict = {
        'Disease': []
        , 'Gene': []
        , 'Chromosome': []
        , 'DBDSMScore': []
            }
    result = np.array(list(result))
    i = 0
    for flagkey in flags.keys():
        if flags[flagkey] == 1:
            continue
        dict[flagkey] = list(np.unique(result[:, i+2]))
        i += 1

    for key in list(dict.keys()):
        if len(dict[key]) == 0:
            dict.pop(key)
    return dict

@searchblue.route('/researchDisease', methods=['GET','POST'])
def researchDisease():
    Disease = request.args.get("Disease")
    dict = {
        'Disease': Disease
        , 'Gene': ''
        , 'Chromosome': ''
        , 'DBDSMScore': ''
            }
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    paginate = showAdvancedTable(dict, page, per_page)
    return render_template('searchresult2.html',page=page,per_page=per_page, pagination=paginate, Disease=Disease, Gene='', Chromosome='', DBDSMScore='')


@searchblue.route('/researchGene', methods=['GET','POST'])
def researchGene():
    reGene = request.args.get("reGene")
    dict = {
        'Disease': ''
        , 'Gene': reGene
        , 'Chromosome': ''
        , 'DBDSMScore': ''
            }
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    paginate = showAdvancedTable(dict, page, per_page)
    # print(paginate)
    return render_template('searchresult2.html',page=page,per_page=per_page, pagination=paginate, Disease=None, Gene=reGene, Chromosome=None, DBDSMScore=None)


@searchblue.route('/test', methods=['GET', 'POST'])
def test():
    '''
    测试
    :return:
    '''
    return render_template('search2.html')



# @searchblue.route('/searchTable', methods=['GET', 'POST'])
# def searchTable():
#     form = SearchForm()
#     page = request.args.get("page", 1, type=int)
#     per_page = request.args.get("per_page", 10, type=int)
#     if request.method == "POST" or form.validate_on_submit():
#         searchBy = form.searchBy.data[0]
#         userinput = form.userinput.data
#         print(searchBy)
#         paginate = showTable((searchBy, userinput), page, per_page)
#         return render_template('searchresult.html', searchBy=searchBy, userinput=userinput, pagination=paginate, search_result=searchBy+' like:'+userinput)
#     if request.method == "GET" and form.validate_on_submit():
#         form.searchBy.data = 'Disease'
#         return render_template("search.html", form=form)


# @searchblue.route('/?<string:searchBy>&<string:userinput>')
# def searchTable(searchBy,userinput):
#     page = request.args.get("page", 1, type=int)
#     per_page = request.args.get("per_page", 5, type=int)
#     paginate = showTable((searchBy, userinput), page, per_page)
#     return render_template('searchresult.html', searchBy=searchBy, userinput=userinput, pagination=paginate, search_result=searchBy+' like:'+userinput)

# @searchblue.route('/searchTable', methods=['GET', 'POST'])
# def searchTable2():
#     page = request.args.get("page", 1, type=int)
#     per_page = request.args.get("per_page", 5, type=int)
#     searchBy = request.args.get("searchBy")
#     userinput = request.args.get("userinput")
#     print(searchBy,userinput)
#     paginate = showTable((searchBy, userinput), page, per_page)
#     return render_template('searchresult.html', searchBy=searchBy, userinput=userinput, pagination=paginate, search_result=str(searchBy)+' like:'+str(userinput))



#下面这是数据库载入的代码
# import pandas as pd
# @searchblue.route('/addall')
# def addAllSql():
#     data = pd.read_csv('C:/Users/whd/Desktop/7-2/DSMv2.csv',dtype=str , encoding='ISO-8859-1')
#     for line in data.values:
#         allDataInfo = AllData(
#         DBDSMID = str(line[0]),
#         Disease =  str(line[1]),
#         DOID =  str(line[2]),
#         Gene =  str(line[3]),
#         GeneID =  str(line[4]),
#         MIM =  str(line[5]),
#         Map_Location =  str(line[6]),
#         VariantType =  str(line[7]),
#         Protein =  str(line[8]),
#         cDNA =  str(line[9]),
#         SNPID =  str(line[10]),
#         CodonChange =  str(line[11]),
#         RefseqTranscript =  str(line[12]),
#         P_Value =  str(line[13]),
#         Strand =  str(line[14]),
#         GRCh38_Position =  str(line[15]),
#         GRCh37_Position =  str(line[16]),
#         Ref =  str(line[17]),
#         Alt =  str(line[18]),
#         Year =  str(line[19]),
#         PMID =  str(line[20]),
#         Ethnicity =  str(line[21]),
#         Classification =  str(line[22]),
#         StrengthOfEvidence =  str(line[23]),
#         KeySentence =  str(line[24]),
#         PhyloP100way =  str(line[25]),
#         PhastCons100way =  str(line[26]),
#         GerpS =  str(line[27]),
#         Silva =  str(line[28]),
#         DDIG =  str(line[29]),
#         FATHMM_MKL =  str(line[30]),
#         CADD =  str(line[31]),
#         Trap =  str(line[32]),
#         DBDSMScore =  str(line[33]),
#         Source =  str(line[34]),
#         Chromosome = 'nan' if str(line[15]) == 'nan' else str(line[15]).split(':')[0]
#         )
#         db.session.add(allDataInfo)
#         # break
#     db.session.commit()
#     print('ok!')
#     return render_template("success.html")



