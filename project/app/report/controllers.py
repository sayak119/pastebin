from flask import Blueprint, request, session, jsonify, render_template
from sqlalchemy.exc import IntegrityError
from app import db, requires_auth
from .models import Report
from app.paste.models import Paste
from datetime import datetime
from dateutil import parser

mod_report = Blueprint('report', __name__)

def is_active(paste):
	return parser.parse(paste.expire_time) > datetime.now()

@mod_report.route('/<url>/add_report', methods=['POST'])
@requires_auth
def add_report(url):
    try:
        paste_id = url
        reason = request.form['reason']
        reporter_id = session['user_id']

    except KeyError as e:
        return (jsonify(success=False, message="%s not sent in the request" % e.args), 400)

    paste = Paste.query.filter(Paste.url == paste_id).first()
    if is_active(paste):
        report_check_list = Report.query.filter(
            Report.reporter_id == reporter_id, Report.paste_id == paste_id).all()
        if paste.user_id == reporter_id:
            return jsonify({'error':'Cannot Report your own paste'}),400
        # if len(report_check_list) != 0:
        #     return jsonify({'error':'You have already reported the paste','length':len(report_check_list)}),400
        rep = Report(paste_id, reason, reporter_id)
        if(paste.report_count >= 5):
            delete_rep_list = Report.query.filter(Report.paste_id == paste.url).all()
            for delete_rep in delete_rep_list:
                db.session.delete(delete_rep)
            db.session.delete(paste)
        else:
            db.session.add(rep)
            x = paste.report_count
            paste.report_count = x + 1
        db.session.commit()

        return render_template('user.html'),200

    else:
        db.session.delete(paste)
        db.session.commit()
        return render_template('index.html'),404


@mod_report.route('/<url>/add_report', methods=['GET'])
@requires_auth
def get_form(url):
    paste = Paste.query.filter(Paste.url == url).first()
    if is_active(paste):
        return render_template('report.html', report_id=url)
    else:
        db.session.delete(paste)
        db.session.commit()
        return render_template('index.html'),404
