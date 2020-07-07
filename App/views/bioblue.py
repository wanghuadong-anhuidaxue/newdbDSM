from flask import Blueprint, render_template, session, escape, redirect, url_for, request

from App.models import db, User, BioInfo

bioblue = Blueprint("bioblue", __name__, url_prefix="/bio")


@bioblue.route('/')
def bioindex():
    username = session.get('username')
    password = session.get('password')

    if username is not None:
        db_user = User.query.filter_by(username=username).first()
        db_bioInfo_list = BioInfo.query.all()
        if db_user is not None:
            if username == db_user.username and password == db_user.password:
                # print(db_user.username+db_user.password)
                return render_template('index.html', username=session.get('username'), db_bioInfo_list=db_bioInfo_list)
        else:
            print('ERRoR')
    return redirect(url_for('userblue.login'))


@bioblue.route('/add')
def addBioInfo():
    return render_template('add.html')

@bioblue.route('/addBioInfoSubmit', methods=['post', 'get'])
def addBioInfoSubmit():
    bioname = request.form.get('bioname')
    bioinfo = request.form.get('bioinfo')
    print(bioname+bioinfo)
    bioInfo = BioInfo(bioname=bioname, bioinfo=bioinfo)
    db.session.add(bioInfo)
    db.session.commit()
    return redirect(url_for('bioblue.bioindex'))


@bioblue.route('/deleteBioInfoSubmit', methods=['post', 'get', 'put'])
def deleteBioInfoSubmit():
    bioid = request.args['bioid']
    db_bioInfo = BioInfo.query.filter_by(id=bioid).first()
    db.session.delete(db_bioInfo)
    db.session.commit()
    return redirect(url_for('bioblue.bioindex'))


@bioblue.route('/upgradeBioInfo')
def upgradeBioInfo():
    bioid = request.args['bioid']
    bioInfo = BioInfo.query.filter_by(id=bioid).first()
    return render_template('upgrade_bio.html', bioInfo=bioInfo)


@bioblue.route('/upgradeBioInfoSubmit', methods=['post', 'get', 'put'])
def upgradeBioInfoSubmit():
    bioid = request.form.get('bioid')
    bioname = request.form.get('bioname')
    bioinfo = request.form.get('bioinfo')
    BioInfo.query.filter_by(id=bioid).update({'bioname': bioname, 'bioinfo': bioinfo})
    db.session.commit()
    return redirect(url_for('bioblue.bioindex'))


