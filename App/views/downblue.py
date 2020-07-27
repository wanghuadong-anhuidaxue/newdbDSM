from flask import Blueprint, render_template, request, redirect, url_for, jsonify,current_app, send_from_directory

from App.tools import downShowTable, sQLAlchemyToCsv, random_filename, downShowAdvancedTable


downblue = Blueprint("downblue", __name__)





@downblue.route('/downAllTable')
def downAllTable():
    userinput = request.args.get("userinput")
    searchBy = request.args.get("searchBy")
    result = downShowTable([searchBy, userinput])
    filename = random_filename('')+'.csv'
    sQLAlchemyToCsv(result).to_csv(str(current_app.config['DOWNTABLE_PATH'])+'\\'+filename, index=False)
    return send_from_directory(str(current_app.config['DOWNTABLE_PATH']),filename=filename,as_attachment=True)#redirect(url_for('/newdbDSM/'+filename))


@downblue.route('/downAllTable2')
def downAllTable2():
    dict = {
        'Disease': request.args.get('Disease')
        , 'Gene': request.args.get('Gene')
        , 'Chromosome': request.args.get('Chromosome')
        , 'Classification': request.args.get('Classification')
        , 'StrengthOfEvidence': request.args.get('StrengthOfEvidence')
    }
    result = downShowAdvancedTable(dict)
    filename = random_filename('')+'.csv'
    sQLAlchemyToCsv(result).to_csv(str(current_app.config['DOWNTABLE_PATH'])+'\\'+filename, index=False)
    return send_from_directory(str(current_app.config['DOWNTABLE_PATH']),filename=filename,as_attachment=True)#redirect(url_for('/newdbDSM/'+filename))



@downblue.route('/downResult')
def downResult():
    filename = request.args.get('filename')
    return send_from_directory(str(current_app.config['RESULT_PATH']),filename=filename,as_attachment=True)#redirect(url_for('/newdbDSM/'+filename))
