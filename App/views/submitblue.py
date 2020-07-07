
from flask import Blueprint, render_template, request, redirect, url_for
from .forms import SubmitForm #导入本地写的forms.py
from App.models import db, Tbsubmit

submitblue = Blueprint("submitblue", __name__)


@submitblue.route('/submit')
@submitblue.route('/newdbDSM/submit', methods=['GET','POST'])
def submit():
    form = SubmitForm()

    if form.validate_on_submit():
        title = form.title.data
        joumal = form.joumal.data
        gene = form.gene.data
        email = form.email.data
        mutation = form.mutation.data
        more = form.more.data
        print(title, joumal, gene, email, mutation, more)
        saveSubmit(title, joumal, gene, email, mutation, more)
        return redirect(url_for('submitblue.submitSuccess'))

    return render_template("submit.html", form=form)


def saveSubmit(title, joumal, gene, email, mutation, more):
    tbsubmitInfo = Tbsubmit(title=title, joumal=joumal, gene=gene, email=email, mutation=mutation, more=more)
    db.session.add(tbsubmitInfo)
    db.session.commit()
    print('sql save success!!')
    # return redirect(url_for('bioblue.bioindex'))


@submitblue.route('/newdbDSM/submitsuccess', methods=['GET','POST'])
def submitSuccess():
    form = SubmitForm()
    print('hahahah')
    return render_template("submit.html", form=form, status=1)


