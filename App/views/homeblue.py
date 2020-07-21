
from flask import Blueprint, render_template, session, escape, redirect, url_for, request
from App.tools import numpy as np
from App.models import db, AllData

homeblue = Blueprint("homeblue",__name__)



@homeblue.route('/')
@homeblue.route('/newdbDSM/')
def index():
    return render_template("index.html")





@homeblue.route('/download')
@homeblue.route('/newdbDSM/download')
def download():
    return render_template("download.html")


@homeblue.route('/about')
@homeblue.route('/newdbDSM/about')
def about():
    mRNA_structure = np.load('aboutdata/mRNA_structure.npy')
    microRNA_binding = np.load('aboutdata/microRNA_binding.npy')
    Protein_synthesis = np.load('aboutdata/Protein_synthesis.npy')
    Splicing_regulation = np.load('aboutdata/Splicing_regulation.npy')
    Transcription_factor_regulation = np.load('aboutdata/Transcription_factor_regulation.npy')
    Specific_methods = np.load('aboutdata/Specific_methods.npy')
    General_methods = np.load('aboutdata/General_methods.npy')
    Analysis_articles = np.load('aboutdata/Analysis_articles.npy')
    Review_articels = np.load('aboutdata/Review_articels.npy')
    return render_template("about.html", literatureALLList=[mRNA_structure,microRNA_binding,Protein_synthesis,Splicing_regulation,Transcription_factor_regulation,Specific_methods
                                                            ,General_methods,Analysis_articles,Review_articels])



@homeblue.route('/contact')
@homeblue.route('/newdbDSM/contact')
def contact():
    return render_template("contact.html")
