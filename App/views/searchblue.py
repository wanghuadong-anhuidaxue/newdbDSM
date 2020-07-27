from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .forms import SearchForm  # ,AdvancedSearchForm #导入本地写的forms.py
from App.models import db, AllData
from App.tools import changeHTML, result_to_dict, showAdvancedTable, showTable # 导入自制工具包
from sqlalchemy import or_, and_
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
def searchTable():#page, per_page, searchBy, userinput
    '''
    表单更新
    :return:使用的是request.args调用
    '''
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    searchBy = request.args.get("searchBy")
    userinput = request.args.get("userinput")
    # print(page,per_page,searchBy,userinput)
    paginate = showTable((searchBy, userinput), page, per_page)
    return render_template('searchresult.html', page=page, per_page=per_page, searchBy=searchBy, userinput=userinput,
                           pagination=paginate)


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


@searchblue.route('/resetPageLimit1', methods=['GET', 'POST'])
def resetPageLimit1():
    newlimit = int(request.args.get('newlimit'))
    searchBy = request.args.get('searchBy')
    userinput = request.args.get("userinput")
    return redirect(url_for('searchblue.searchTable', page=1, per_page=newlimit, userinput=userinput, searchBy=searchBy))



# 下面这是数据库载入的代码
@searchblue.route('/addall')
def addAllSql():
    import pandas as pd
    data = pd.read_csv('C:/Users/whd/PycharmProjects/newdbDSM/DSMv2.1.1.csv', dtype=str, encoding='ISO-8859-1')
    for line in data.values:
        allDataInfo = AllData(
            DBDSMID=str(line[0]),
            Disease=str(line[1]),
            DOID='n/a' if str(line[2]) == 'nan' else str(line[2]),
            Gene='n/a' if str(line[3]) == 'nan' else str(line[3]),
            GeneID='n/a' if str(line[4]) == 'nan' else str(line[4]),
            MIM='n/a' if str(line[5]) == 'nan' else str(line[5]),
            Map_Location='n/a' if str(line[6]) == 'nan' else str(line[6]),
            VariantType='n/a' if str(line[7]) == 'nan' else str(line[7]),
            Protein='n/a' if str(line[8]) == 'nan' else str(line[8]),
            cDNA='n/a' if str(line[9]) == 'nan' else str(line[9]),
            SNPID='n/a' if str(line[10]) == 'nan' else str(line[10]),
            CodonChange='n/a' if str(line[11]) == 'nan' else str(line[11]),
            RefseqTranscript='n/a' if str(line[12]) == 'nan' else str(line[12]),
            P_Value='n/a' if str(line[13]) == 'nan' else str(line[13]),
            Strand='n/a' if str(line[14]) == 'nan' else str(line[14]),
            GRCh38_Position='n/a' if str(line[15]) == 'nan' else str(line[15]),
            GRCh37_Position='n/a' if str(line[16]) == 'nan' else str(line[16]),
            Ref='n/a' if str(line[17]) == 'nan' else str(line[17]),
            Alt='n/a' if str(line[18]) == 'nan' else str(line[18]),
            Year='n/a' if str(line[19]) == 'nan' else str(line[19]),
            PMID='n/a' if str(line[20]) == 'nan' else str(line[20]),
            Ethnicity='n/a' if str(line[21]) == 'nan' else str(line[21]),
            Classification='n/a' if str(line[22]) == 'nan' else str(line[22]),
            StrengthOfEvidence='n/a' if str(line[23]) == 'nan' else str(line[23]),
            KeySentence='n/a' if str(line[24]) == 'nan' else str(line[24]),
            PrDSM='n/a' if str(line[26]) == 'nan' else str(line[26]),
            TraP='n/a' if str(line[27]) == 'nan' else str(line[27]),
            PhD_SNPg='n/a' if str(line[28]) == 'nan' else str(line[28]),
            FATHMM_MKL='n/a' if str(line[29]) == 'nan' else str(line[29]),
            CADD='n/a' if str(line[30]) == 'nan' else str(line[30]),
            DANN='n/a' if str(line[31]) == 'nan' else str(line[31]),
            FATHMM_XF='n/a' if str(line[32]) == 'nan' else str(line[32]),
            priPhCons='n/a' if str(line[33]) == 'nan' else str(line[33]),
            mamPhCons='n/a' if str(line[34]) == 'nan' else str(line[34]),
            verPhCons='n/a' if str(line[35]) == 'nan' else str(line[35]),
            priPhyloP='n/a' if str(line[36]) == 'nan' else str(line[36]),
            mamPhyloP='n/a' if str(line[37]) == 'nan' else str(line[37]),
            verPhyloP='n/a' if str(line[38]) == 'nan' else str(line[38]),
            GerpS='n/a' if str(line[39]) == 'nan' else str(line[39]),
            TFBs='n/a' if str(line[40]) == 'nan' else str(line[40]),
            TE='n/a' if str(line[41]) == 'nan' else str(line[41]),
            dPSIZ='n/a' if str(line[42]) == 'nan' else str(line[42]),
            DSP='n/a' if str(line[43]) == 'nan' else str(line[43]),
            Source='n/a' if str(line[25]) == 'nan' else str(line[25]),
            Chromosome='n/a' if str(line[15]) == 'nan' else str(line[15]).split(':')[0]
        )
        db.session.add(allDataInfo)
        # break
    db.session.commit()
    print('ok!')
    return render_template("success.html")
