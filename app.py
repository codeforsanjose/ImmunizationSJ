#!/usr/bin/python
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, jsonify, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'immune.db'),
    DEBUG=True,
    SECRET_KEY='HQQbsqey6R3TBwhCC17sTSAySerXwiAmsvDhm7Tbe8FFTIIWzhOkIA',
    USERNAME='admin',
    PASSWORD='password'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

records = [
{"PUBLIC/  PRIVATE": "PUBLIC", "# CONDITIONAL": "", "% VARI": "", "% HEPB": "", "% MMR": "", "# PRE-JAN PBE": "", "# PME": "", "SCHOOL NAME": "ALAMEDA COUNTY COMMUNITY", "% PBE": "", "# HEALTH CARE PRACTITIONER COUNSELED PBE": "", "# VARI": "", "# UP-TO-DATE": "", "# MMR": "", "% CONDITIONAL": "", "# DTP": "", "COUNTY": "ALAMEDA", "REPORTED": "N", "% DTP": "", "# POLIO": "", "% UP-TO-DATE": "", "CITY": "HAYWARD", "# RELIGIOUS PBE": "", "PUBLIC SCHOOL DISTRICT": "ALAMEDA COUNTY OFFICE OF EDUCATION", "# HEPB": "", "# PBE": "", "ENROLLMENT": " ", "% POLIO": "", "% RELIGIOUS PBE": "", "% PME": "", "SCHOOL CODE": 130419, "% HEALTH CARE PRACTITIONER COUNSELED PBE": "", "% PRE-JAN PBE": ""},
{"PUBLIC/  PRIVATE": "PUBLIC", "# CONDITIONAL": "0", "% VARI": "87", "% HEPB": "87", "% MMR": "87", "# PRE-JAN PBE": "0", "# PME": "0", "SCHOOL NAME": "FAME PUBLIC CHARTER", "% PBE": "13", "# HEALTH CARE PRACTITIONER COUNSELED PBE": "0", "# VARI": "95", "# UP-TO-DATE": "95", "# MMR": "95", "% CONDITIONAL": "0", "# DTP": "95", "COUNTY": "ALAMEDA", "REPORTED": "Y", "% DTP": "87", "# POLIO": "95", "% UP-TO-DATE": "87", "CITY": "NEWARK", "# RELIGIOUS PBE": "14", "PUBLIC SCHOOL DISTRICT": "ALAMEDA COUNTY OFFICE OF EDUCATION", "# HEPB": "95", "# PBE": "14", "ENROLLMENT": "109", "% POLIO": "87", "% RELIGIOUS PBE": "13", "% PME": "0", "SCHOOL CODE": 109835, "% HEALTH CARE PRACTITIONER COUNSELED PBE": "0", "% PRE-JAN PBE": "0"},
{"PUBLIC/  PRIVATE": "PUBLIC", "# CONDITIONAL": "", "% VARI": "", "% HEPB": "", "% MMR": "", "# PRE-JAN PBE": "", "# PME": "", "SCHOOL NAME": "COMMUNITY SCHOOL FOR CREATIVE EDUCATION", "% PBE": "", "# HEALTH CARE PRACTITIONER COUNSELED PBE": "", "# VARI": "", "# UP-TO-DATE": "", "# MMR": "", "% CONDITIONAL": "", "# DTP": "", "COUNTY": "ALAMEDA", "REPORTED": "N", "% DTP": "", "# POLIO": "", "% UP-TO-DATE": "", "CITY": "OAKLAND", "# RELIGIOUS PBE": "", "PUBLIC SCHOOL DISTRICT": "ALAMEDA COUNTY OFFICE OF EDUCATION", "# HEPB": "", "# PBE": "", "ENROLLMENT": " ", "% POLIO": "", "% RELIGIOUS PBE": "", "% PME": "", "SCHOOL CODE": 123968, "% HEALTH CARE PRACTITIONER COUNSELED PBE": "", "% PRE-JAN PBE": ""},
{"PUBLIC/  PRIVATE": "PUBLIC", "# CONDITIONAL": "25", "% VARI": "92", "% HEPB": "90", "% MMR": "90", "# PRE-JAN PBE": "0", "# PME": "1", "SCHOOL NAME": "COX ACADEMY", "% PBE": "1", "# HEALTH CARE PRACTITIONER COUNSELED PBE": "0", "# VARI": "106", "# UP-TO-DATE": "88", "# MMR": "103", "% CONDITIONAL": "22", "# DTP": "103", "COUNTY": "ALAMEDA", "REPORTED": "Y", "% DTP": "90", "# POLIO": "105", "% UP-TO-DATE": "77", "CITY": "OAKLAND", "# RELIGIOUS PBE": "1", "PUBLIC SCHOOL DISTRICT": "ALAMEDA COUNTY OFFICE OF EDUCATION", "# HEPB": "104", "# PBE": "1", "ENROLLMENT": "115", "% POLIO": "91", "% RELIGIOUS PBE": "1", "% PME": "1", "SCHOOL CODE": 6001788, "% HEALTH CARE PRACTITIONER COUNSELED PBE": "0", "% PRE-JAN PBE": "0"},
{"PUBLIC/  PRIVATE": "PUBLIC", "# CONDITIONAL": "4", "% VARI": "98", "% HEPB": "95", "% MMR": "100", "# PRE-JAN PBE": "0", "# PME": "0", "SCHOOL NAME": "LAZEAR CHARTER ACADEMY", "% PBE": "0", "# HEALTH CARE PRACTITIONER COUNSELED PBE": "0", "# VARI": "39", "# UP-TO-DATE": "36", "# MMR": "40", "% CONDITIONAL": "10", "# DTP": "36", "COUNTY": "ALAMEDA", "REPORTED": "Y", "% DTP": "90", "# POLIO": "38", "% UP-TO-DATE": "90", "CITY": "OAKLAND", "# RELIGIOUS PBE": "0", "PUBLIC SCHOOL DISTRICT": "ALAMEDA COUNTY OFFICE OF EDUCATION", "# HEPB": "38", "# PBE": "0", "ENROLLMENT": "40", "% POLIO": "95", "% RELIGIOUS PBE": "0", "% PME": "0", "SCHOOL CODE": 6002000, "% HEALTH CARE PRACTITIONER COUNSELED PBE": "0", "% PRE-JAN PBE": "0"},
{"PUBLIC/  PRIVATE": "PUBLIC", "# CONDITIONAL": "", "% VARI": "", "% HEPB": "", "% MMR": "", "# PRE-JAN PBE": "", "# PME": "", "SCHOOL NAME": "URBAN MONTESSORI CHARTER", "% PBE": "", "# HEALTH CARE PRACTITIONER COUNSELED PBE": "", "# VARI": "", "# UP-TO-DATE": "", "# MMR": "", "% CONDITIONAL": "", "# DTP": "", "COUNTY": "ALAMEDA", "REPORTED": "N", "% DTP": "", "# POLIO": "", "% UP-TO-DATE": "", "CITY": "OAKLAND", "# RELIGIOUS PBE": "", "PUBLIC SCHOOL DISTRICT": "ALAMEDA COUNTY OFFICE OF EDUCATION", "# HEPB": "", "# PBE": "", "ENROLLMENT": " ", "% POLIO": "", "% RELIGIOUS PBE": "", "% PME": "", "SCHOOL CODE": 125567, "% HEALTH CARE PRACTITIONER COUNSELED PBE": "", "% PRE-JAN PBE": ""},
{"PUBLIC/  PRIVATE": "PUBLIC", "# CONDITIONAL": "0", "% VARI": "90", "% HEPB": "90", "% MMR": "90", "# PRE-JAN PBE": "0", "# PME": "0", "SCHOOL NAME": "YU MING CHARTER", "% PBE": "10", "# HEALTH CARE PRACTITIONER COUNSELED PBE": "0", "# VARI": "47", "# UP-TO-DATE": "47", "# MMR": "47", "% CONDITIONAL": "0", "# DTP": "47", "COUNTY": "ALAMEDA", "REPORTED": "Y", "% DTP": "90", "# POLIO": "47", "% UP-TO-DATE": "90", "CITY": "OAKLAND", "# RELIGIOUS PBE": "5", "PUBLIC SCHOOL DISTRICT": "ALAMEDA COUNTY OFFICE OF EDUCATION", "# HEPB": "47", "# PBE": "5", "ENROLLMENT": "52", "% POLIO": "90", "% RELIGIOUS PBE": "10", "% PME": "0", "SCHOOL CODE": 124172, "% HEALTH CARE PRACTITIONER COUNSELED PBE": "0", "% PRE-JAN PBE": "0"},
{"PUBLIC/  PRIVATE": "PUBLIC", "# CONDITIONAL": "", "% VARI": "", "% HEPB": "", "% MMR": "", "# PRE-JAN PBE": "", "# PME": "", "SCHOOL NAME": "ALAMEDA COUNTY JUVENILE HALL COURT", "% PBE": "", "# HEALTH CARE PRACTITIONER COUNSELED PBE": "", "# VARI": "", "# UP-TO-DATE": "", "# MMR": "", "% CONDITIONAL": "", "# DTP": "", "COUNTY": "ALAMEDA", "REPORTED": "N", "% DTP": "", "# POLIO": "", "% UP-TO-DATE": "", "CITY": "SAN LEANDRO", "# RELIGIOUS PBE": "", "PUBLIC SCHOOL DISTRICT": "ALAMEDA COUNTY OFFICE OF EDUCATION", "# HEPB": "", "# PBE": "", "ENROLLMENT": " ", "% POLIO": "", "% RELIGIOUS PBE": "", "% PME": "", "SCHOOL CODE": 130401, "% HEALTH CARE PRACTITIONER COUNSELED PBE": "", "% PRE-JAN PBE": ""},
{"PUBLIC/  PRIVATE": "PUBLIC", "# CONDITIONAL": "1", "% VARI": "98", "% HEPB": "98", "% MMR": "98", "# PRE-JAN PBE": "0", "# PME": "0", "SCHOOL NAME": "AMELIA EARHART ELEMENTARY", "% PBE": "2", "# HEALTH CARE PRACTITIONER COUNSELED PBE": "2", "# VARI": "126", "# UP-TO-DATE": "125", "# MMR": "125", "% CONDITIONAL": "1", "# DTP": "126", "COUNTY": "ALAMEDA", "REPORTED": "Y", "% DTP": "98", "# POLIO": "126", "% UP-TO-DATE": "98", "CITY": "ALAMEDA", "# RELIGIOUS PBE": "0", "PUBLIC SCHOOL DISTRICT": "ALAMEDA UNIFIED", "# HEPB": "126", "# PBE": "2", "ENROLLMENT": "128", "% POLIO": "98", "% RELIGIOUS PBE": "0", "% PME": "0", "SCHOOL CODE": 6100374, "% HEALTH CARE PRACTITIONER COUNSELED PBE": "2", "% PRE-JAN PBE": "0"}
]


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, DATABASE_NAME):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, DATABASE_NAME):
        g.sqlite_db.close()


@app.route('/', methods=['GET'])
def get_records():
    return jsonify({'records': records})



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/<int:school_code>', methods=['GET'])
def get_record(school_code):
	school_code = int(school_code)
	print(school_code)
	record = [record for record in records if records['SCHOOL CODE'] == school_code]
	if len(record) == 0:
		abort(404)
	return jsonify({'records': record[0]})


@app.route('/location', methods=['GET'])
def get_record_by_location():
	city     = request.args.get('city')
	zip_code = request.args.get('zip')
	radius   = request.args.get('radius')
	record_results = []
	if city:
		record_results = [record for record in records if record['CITY'] == city]
	if zip_code:
		record_results = [record for record in records if record['ZIP'] == zip_code]
	
	if len(record_results) == 0:
		abort(404)
	return jsonify({'records': record_results})


if __name__ == '__main__':
    app.run(debug=True)