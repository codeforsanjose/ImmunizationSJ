#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, jsonify, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__)

# Load default config and override config from an environment variable
# CHANGE SECRET_KEY IN PRODUCTION!!!!
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'immune.db'),
    DEBUG=True,
    SECRET_KEY='HQQbsqey6R3TBwhCC17sTSAySerXwiAmsvDhm7Tbe8FFTIIWzhOkIA',
    USERNAME='admin',
    PASSWORD='password'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, app.config['DATABASE']):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, app.config['DATABASE']):
        g.sqlite_db.close()



def dict_factory(cursor, row):
    """a helper method for row_factory"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def get_records(): 
    con = get_db()
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM records JOIN schools on records.school = schools.school_code limit 10")

    if request.args.get('json') is not None:
        return jsonify({'records': cur.fetchall()})
    else:
        return render_template('index.html', records=cur.fetchall())



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
            return redirect(url_for('get_records'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('get_records'))

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/school/<int:school_code>', methods=['GET'])
def get_record(school_code):

    where=[]
    args = {}

    school_code = int(school_code)
    print(school_code)
    where.append('school_code=:school_code')
    args["school_code"] = school_code

    con = get_db()
    con.row_factory = dict_factory
    cur = con.cursor()
    querystring = "SELECT * FROM records JOIN schools on records.school = schools.school_code where " + " and ".join(where)
    print(querystring)
    cur.execute(querystring, args)
    res = cur.fetchone()

    if request.args.get('json') is not None:
        return jsonify({'records': res})
    else:
        return render_template('school.html', school=res)


@app.route('/schools', methods=['GET'])
def get_school_by_advanced():

    advanced_searchables = ['city','district','county']

    where=[]
    args = {}

    is_public = request.args.get('public')
    if is_public is not None:
        is_public = 1 if request.args.get('public').lower() == "true" else 0
        where.append("is_public=:is_public")
        args["is_public"] = is_public

    for metric in advanced_searchables:
        m = request.args.get(metric)
        if m is not None:
            m = m.upper()
            where.append(metric+"=:"+metric)
            args[metric] = m

    if len(where) == 0:
        return jsonify({'records': None})

    con = get_db()
    con.row_factory = dict_factory
    cur = con.cursor()
    querystring = "SELECT * FROM schools where " + " and ".join(where)
    print(querystring)
    cur.execute(querystring, args)
    res = cur.fetchall()

    if request.args.get('json') is not None:
        return jsonify({'records': res})
    else:
        return render_template('schools.html', schools=res)


@app.route('/search', methods=['GET','POST'])
def search():

    searchables = ['school_name','city','district','county']
    search_input = request.form['search']

    if search_input is not None:
        search_input = search_input.upper()

    where=[]
    args = {}

    for metric in searchables:
        where.append(metric+" like :"+metric)
        args[metric] = '%'+search_input+'%'

    con = get_db()
    con.row_factory = dict_factory
    cur = con.cursor()
    querystring = "SELECT * FROM schools where " + " or ".join(where)
    print(querystring)
    cur.execute(querystring, args)
    res = cur.fetchall()

    if len(res) > 5000:
        flash('Too many search results!')
        return redirect(url_for('get_records'))

    if request.args.get('json') is not None:
        return jsonify({'records': res})
    else:
        return render_template('schools.html', schools=res)


if __name__ == '__main__':
    app.run(debug=True)