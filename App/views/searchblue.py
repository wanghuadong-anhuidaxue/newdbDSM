from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .forms import SearchForm  # ,AdvancedSearchForm #导入本地写的forms.py
from App.models import db, AllData
from App.tools import objectStarToNo, changeHTML  # 导入自制工具包
from sqlalchemy import or_, and_
from jinja2 import escape
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
    form.searchBy.data = 'Disease'  # 默认选择，不然就是中文的请选择了
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
        paginate = AllData.query.filter(AllData.Disease.like('%' + userinput + '%')).paginate(page, limit, False)
    elif searchBy == 'Gene':
        paginate = AllData.query.filter(AllData.Gene.like('%' + userinput + '%')).paginate(page, limit, False)
    elif searchBy == 'GRCh38_Position':
        paginate = AllData.query.filter(AllData.GRCh38_Position.like('%' + userinput + '%')).paginate(page, limit,
                                                                                                      False)
    elif searchBy == 'Mutation':
        paginate = AllData.query.filter(or_(AllData.Protein.like('%' + userinput + '%'),
                                            AllData.cDNA.like('%' + userinput + '%'),
                                            AllData.SNPID.like('%' + userinput + '%'))).paginate(page, limit, False)
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

    userinput = changeHTML(userinput)
    paginate = showTable((searchBy, userinput), page, per_page)
    return render_template('searchresult.html', searchBy=searchBy, userinput=userinput, pagination=paginate,
                           search_result=searchBy + ' like:' + userinput)


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
    return render_template('searchresult.html', page=page, per_page=per_page, searchBy=searchBy, userinput=userinput,
                           pagination=paginate, search_result=searchBy + ' like:' + userinput)


@searchblue.route('/detailScore', methods=['GET', 'POST'])
def detailScore():
    dbid = request.args.get("dbid")
    result = AllData.query.filter_by(dbid=dbid).first()
    return render_template('details2.html', dbDSMData=result)


@searchblue.route('/advancedSearch', methods=['GET'])
def advancedSearch():
    Disease = request.args.get('Disease')
    Gene = request.args.get('Gene')
    Chromosome = request.args.get('Chromosome')
    Classification = request.args.get('Classification')
    StrengthOfEvidence = request.args.get('StrengthOfEvidence')
    flags = {'Disease': 1, 'Gene': 1, 'Chromosome': 1, 'Classification':1, 'StrengthOfEvidence':1}  # 立标签
    sql = 'select dbid,DBDSMID' \
          + (",Disease" if (Disease == "" or Disease == None) else "") \
          + (",Gene" if (Gene == "" or Gene == None) else "") \
          + (",Chromosome" if (Chromosome == "" or Chromosome == None) else "") \
          + (",Classification" if (Classification == "" or Classification == None) else "") \
          + (",StrengthOfEvidence" if (StrengthOfEvidence == "" or StrengthOfEvidence == None) else "") \
          + " from all_data where DBDSMID like '%'" \
          + ("" if (Disease == "" or Disease == None) else (' and Disease="%s"' % Disease)) \
          + ("" if (Gene == "" or Gene == None) else (' and Gene="%s"' % Gene)) \
          + ("" if (Chromosome == "" or Chromosome == None) else (' and Chromosome="%s"' % Chromosome))\
          + ("" if (Classification == "" or Classification == None) else (' and Classification="%s"' % Classification))\
          + ("" if (StrengthOfEvidence == "" or StrengthOfEvidence == None) else (' and StrengthOfEvidence="%s"' % StrengthOfEvidence))+ ';'
    # print('sql__!!:', sql)
    result = db.session.execute(sql)
    if (Disease == "" or Disease == None):
        flags['Disease'] = 0
    if (Gene == "" or Gene == None):
        flags['Gene'] = 0
    if (Chromosome == "" or Chromosome == None):
        flags['Chromosome'] = 0
    if (Classification == "" or Classification == None):
        flags['Classification'] = 0
    if (StrengthOfEvidence == "" or StrengthOfEvidence == None):
        flags['StrengthOfEvidence'] = 0

    payload = result_to_dict(result, flags)  # 转为字典

    # print(payload)
    # print(flags)
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
    Classification = request.args.get('Classification')
    StrengthOfEvidence = request.args.get('StrengthOfEvidence')
    dict = {
        'Disease': Disease
        , 'Gene': Gene
        , 'Chromosome': Chromosome
        , 'Classification': Classification
        , 'StrengthOfEvidence': StrengthOfEvidence
    }
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    # print('dict',dict)
    paginate = showAdvancedTable(dict, page, per_page)
    # print(paginate.items)
    return render_template('searchresult2.html', page=page, per_page=per_page, pagination=paginate, Disease=Disease,
                           Gene=Gene, Chromosome=Chromosome , Classification=Classification, StrengthOfEvidence=StrengthOfEvidence)


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
    Classification = dict['Classification']
    StrengthOfEvidence = dict['StrengthOfEvidence']
    return AllData.query.filter(AllData.Gene.like('%' + "" if (Gene == "" or Gene == None) else Gene + '%'),
                                     AllData.Disease.like('%' + "" if (Disease == "" or Disease == None) else Disease + '%'),
                                     AllData.Chromosome.like('%' + "" if (Chromosome == "" or Chromosome == None) else Chromosome + '%'),
                                     AllData.Classification.like('%' + "" if (Classification == "" or Classification == None) else Classification + '%'),
                                     AllData.StrengthOfEvidence.like('%' + "" if (StrengthOfEvidence == "" or StrengthOfEvidence == None) else StrengthOfEvidence + '%')).paginate(page, limit, False)


def result_to_dict(result, flags):
    '''
    把sql结果转换为对应的字典，方便json传输
    {unique去重，并且拦截nan}
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
        , 'Classification': []
        , 'StrengthOfEvidence': []
    }
    result = np.array(list(result))
    i = 0
    for flagkey in flags.keys():
        if flags[flagkey] == 1:
            continue
        dict[flagkey] = list(np.unique(result[:, i + 2]))#[incom for incom in np.unique(result[:, i + 2]) if str(incom) != 'nan' and str(incom) != 'Other']#unique去重，并且拦截nan
        i += 1

    for key in list(dict.keys()):
        if len(dict[key]) == 0:
            dict.pop(key)
    return dict


@searchblue.route('/researchDisease', methods=['GET', 'POST'])
def researchDisease():
    Disease = request.args.get("Disease")
    dict = {
        'Disease': Disease
        , 'Gene': ''
        , 'Chromosome': ''
        , 'Classification':''
        , 'StrengthOfEvidence':''
    }
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    paginate = showAdvancedTable(dict, page, per_page)
    return render_template('searchresult2.html', page=page, per_page=per_page, pagination=paginate, Disease=Disease,
                           Gene='', Chromosome='',Classification='',StrengthOfEvidence='')


@searchblue.route('/researchGene', methods=['GET', 'POST'])
def researchGene():
    reGene = request.args.get("reGene")
    dict = {
        'Disease': ''
        , 'Gene': reGene
        , 'Chromosome': ''
        , 'Classification': ''
        , 'StrengthOfEvidence': ''
    }
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    paginate = showAdvancedTable(dict, page, per_page)
    # print(paginate)
    return render_template('searchresult2.html', page=page, per_page=per_page, pagination=paginate, Disease='',
                           Gene=reGene, Chromosome='',Classification='',StrengthOfEvidence='')  # 不能写none，会导致查询and_查询无果


# 下面这是数据库载入的代码
@searchblue.route('/addall')
def addAllSql():
    import pandas as pd
    data = pd.read_csv('C:/Users/whd/PycharmProjects/newdbDSM/DSMv2.1.1.csv', dtype=str, encoding='ISO-8859-1')
    for line in data.values:
        allDataInfo = AllData(
            DBDSMID=str(line[0]),
            Disease=str(line[1]),
            DOID=str(line[2]),
            Gene=str(line[3]),
            GeneID=str(line[4]),
            MIM=str(line[5]),
            Map_Location=str(line[6]),
            VariantType=str(line[7]),
            Protein=str(line[8]),
            cDNA=str(line[9]),
            SNPID=str(line[10]),
            CodonChange=str(line[11]),
            RefseqTranscript=str(line[12]),
            P_Value=str(line[13]),
            Strand=str(line[14]),
            GRCh38_Position=str(line[15]),
            GRCh37_Position=str(line[16]),
            Ref=str(line[17]),
            Alt=str(line[18]),
            Year=str(line[19]),
            PMID=str(line[20]),
            Ethnicity=str(line[21]),
            Classification=str(line[22]),
            StrengthOfEvidence=str(line[23]),
            KeySentence=str(line[24]),
            PrDSM=str(line[26]),
            TraP=str(line[27]),
            PhD_SNPg=str(line[28]),
            FATHMM_MKL=str(line[29]),
            CADD=str(line[30]),
            DANN=str(line[31]),
            FATHMM_XF=str(line[32]),
            priPhCons=str(line[33]),
            mamPhCons=str(line[34]),
            verPhCons=str(line[35]),
            priPhyloP=str(line[36]),
            mamPhyloP=str(line[37]),
            verPhyloP=str(line[38]),
            GerpS=str(line[39]),
            TFBs=str(line[40]),
            TE=str(line[41]),
            dPSIZ=str(line[42]),
            DSP=str(line[43]),
            Source=str(line[25]),
            Chromosome='nan' if str(line[15]) == 'nan' else str(line[15]).split(':')[0]
        )
        db.session.add(allDataInfo)
        # break
    db.session.commit()
    print('ok!')
    return render_template("success.html")
