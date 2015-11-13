from flask import render_template,session,redirect,url_for,request,current_app,make_response

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import extract,and_,or_

from flask.ext.wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

from websms import app

import ldap
from datetime import datetime

@app.route('/')
def websms():
    return render_template('index.html')


@app.route('/admin/', methods=['GET', 'POST'])
def options():
    return render_template('admin.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404