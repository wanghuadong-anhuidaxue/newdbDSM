from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from App.models import db, AllData

from sqlalchemy import or_,and_

analysisblue = Blueprint("analysisblue", __name__)



@analysisblue.route('/newdbDSM/analysis')
def analysisIndex():

    return 0