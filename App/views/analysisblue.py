from flask import Blueprint, render_template, request, redirect, url_for, jsonify,current_app
from .forms import AnalysisForm
from App.models import db, AllData
from App.tools import random_filename, os
from App.ext import mail, Message
import time
import subprocess
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

    nowtime = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))

    filename = nowtime+'.vcf'
    mutationPath = Path(current_app.config['UPLOAD_PATH']).joinpath(filename)
    with open(mutationPath, 'w') as f:
        for line in mutation.split('\n'):
            f.write(line)
    resultfilePath = Path(current_app.config['RESULT_PATH']).joinpath(filename)

    findMutation(filename, mutationPath, resultfilePath)#查询突变

    if form.email.data:
        mail_addr = form.email.data
        with open(Path(current_app.config['RESULT_PATH']).joinpath('email.txt'),'a') as f:#记录情况
            f.write('{}\t{}\n'.format(mail_addr,nowtime))
        Subject = 'dbDSM analysis' #发信主题
        Recipients = mail_addr #收件人
        web = '/downResult?filename='
        Body = 'Dear '+str(Recipients)+',\n\nYour dbDSM analysis has been completed.'+web+' Please refer to the attachment.\n\nThank for using dbDSM.\n\n'+ str(time.strftime("%Y-%m-%d", time.localtime()))#邮件内容
        send_email(subject=Subject,to=Recipients,body=Body,resultfile=resultfilePath)
    return render_template('analysisresult.html', filename=filename)


def findMutation(filename, mutationPath, resultfilePath):
    header = 'chr	pos	id	ref	alt	PrDSM	TraP	SilVA	PhD-SNPg	FATHMM-MKL	CADD	DANN	FATHMM-XF	priPhCons	mamPhCons	verPhCons	priPhyloP	mamPhyloP	verPhyloP	GerpS	TFBs	TE	dPSIZ	DSP	RSCU	dRSCU	CpG?	CpG_exon	SR-	SR+	FAS6-	FAS6+	MES	dMES	MES+	MES-	MEC-MC?	MEC-CS?	MES-KM?	PESE-	PESE+	PESS-	PESS+	f_premrna	f_mrna	functional_score_avg	conservation_avg	function_regions_annotation	translation_efficiency	splicing_feature_avg	sequence_feature_avg	score	vote	feature_list	VEP_ensembl_Transcript_ID	VEP_ensembl_Gene_Name	VEP_ensembl_Gene_ID	VEP_ensembl_Protein_ID	VEP_ensembl_HGVSc	VEP_ensembl_HGVSp	VEP_ensembl_STRAND	VEP_refseq_Transcript_ID	VEP_refseq_Gene_Name	VEP_refseq_Gene_ID	VEP_refseq_Protein_ID(ENSP)	VEP_refseq_HGVSc	VEP_refseq_HGVSp	VEP_refseq_STRAND	SnpEff_ensembl_Transcript_ID	SnpEff_ensembl_Gene_name	SnpEff_ensembl_HGVSc	SnpEff_ensembl_HGVSp	SnpEff_refseq_Transcript_ID	SnpEff_refseq_Gene_name	SnpEff_refseq_HGVSc	SnpEff_refseq_HGVSp	ANNOVAR_ensembl_Transcript_ID	ANNOVAR_ensembl_Gene_ID	ANNOVAR_ensembl_HGVSc	ANNOVAR_ensembl_HGVSp	ANNOVAR_refseq_Transcript_ID	ANNOVAR_refseq_Gene_name	ANNOVAR_refseq_HGVSc	ANNOVAR_refseq_HGVSp	ANNOVAR_ucsc_Transcript_ID	ANNOVAR_ucsc_Gene_name	ANNOVAR_ucsc_HGVSc	ANNOVAR_ucsc_HGVSp'
    with open(mutationPath, 'r') as f1, \
        open(resultfilePath, 'w') as f2:
        f2.write(header + '\n')
        for muta in f1:
            muta = muta.strip('\n').split('\t')
            # print(muta)
            cmdStr = 'tabix /data4/chengna/dbDSMv2/anno_feature_transcript/whole_genome_GRCh37_sSNV_featanno.vcf.gz ' + str(
                muta[0]) + ':' + str(muta[1]) + '-' + str(muta[1])
            result = excuteCommand(cmdStr).decode('ISO-8859-1')
            for line in result.split('\n'):
                if line.split('\t')[0:5] == muta:
                    f2.write(str(line) + '\n')



def excuteCommand(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out, err  = ex.communicate()
    ex.wait()
#    print("cmd in:", com)
#    print("cmd out: ", out.decode())
    return out

















