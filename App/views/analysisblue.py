from flask import Blueprint, render_template, request, redirect, url_for, jsonify,current_app
from .forms import AnalysisForm
from App.models import db, AllData
from App.tools import random_filename, os
from App.ext import mail, Message
import time

from pathlib import Path
analysisblue = Blueprint("analysisblue", __name__)


def send_email(subject, to, body, resultfile=''):
    message = Message(subject, recipients=[to], body=body)
    with current_app.open_resource(resultfile) as fp:  # 添加附件
        message.attach(filename='Pred_result.vcf', content_type='text/plain', data=fp.read())  # filename为重命名附件的名字
    mail.send(message)




@analysisblue.route('/newdbDSM/analysis')
def analysisIndex():
    form = AnalysisForm()
    return render_template('analysis.html', form=form)




@analysisblue.route('/newdbDSM/analysisSubmit', methods=['GET', 'POST'])
def analysisSubmit():
    form = AnalysisForm()
    mutation = form.data.data
    # print(mutation)
    nowtime = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    print(nowtime)
    print(current_app.config['UPLOAD_PATH'])
    print(type(mutation))
    filename = nowtime+'.vcf'
    resultfilePath = Path(current_app.config['UPLOAD_PATH']).joinpath(filename)
    with open(resultfilePath, 'w') as f:
        f.write(mutation)


    if form.email.data:
        mail_addr = form.email.data
        with open(Path(current_app.config['RESULT_PATH']).joinpath('email.txt'),'a') as f:
            f.write('{}\t{}\n'.format(mail_addr,nowtime))
        Subject = 'hahahtest' #发信主题
        Recipients = mail_addr#['{}<{}>'.format(mail_addr,mail_addr)]#收件人
        Body = 'Your dbDSM analysis has been completed. Please refer to the attachment.' #邮件内容
        send_email(subject=Subject,to=Recipients,body=Body,resultfile=resultfilePath)
    return render_template('analysisresult.html', filename=filename)





# @analysisblue.route('/newdbDSM/analysisResult', methods=['GET', 'POST'])
# def analysisResult():
#
#     return render_template('analysisresult.html', i=0)



