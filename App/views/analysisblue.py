from flask import Blueprint, render_template, request, redirect, url_for, jsonify,current_app
from .forms import AnalysisForm
from App.models import db, AllData
from App.tools import random_filename, os
from sqlalchemy import or_,and_

analysisblue = Blueprint("analysisblue", __name__)



@analysisblue.route('/newdbDSM/analysis', methods=['GET', 'POST'])
def analysisIndex():
    form = AnalysisForm()
    if form.validate_on_submit():
        if form.uploaddata.data == None:
            print(len(form.data.data))
            print('hahahNone')
        else:
            f = form.uploaddata.data
            filename = random_filename(f.filename)
            f.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
            print('Upload Success!')
            return redirect(url_for('analysisSubmit'))
    return render_template('analysis.html', form=form)




@analysisblue.route('/analysisSubmit', methods=['GET', 'POST'])
def analysisSubmit():
    # uploaddata = request.form.get("uploaddata")
    # data = request.form.get("data")
    # email = request.form.get("email")
    # print(data,email)
    return render_template('success.html')