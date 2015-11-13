from flask import render_template,session,redirect,url_for,request,current_app,make_response

## from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import extract,and_,or_

from websms import app
from websms.database import db
from websms.models import AlertsSubscriberData

import ldap
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def websms():
    debug = None
    if request.method == 'POST':
        phone = request.form['phone-number']

        subscriber = AlertsSubscriberData.query.filter_by(number = phone).first()

        if subscriber:
            return render_template('index.html',update=True,phone=phone,user=subscriber,debug=debug)
        else:
            debug = "No user found, create entry"
            return render_template('index.html',update=True,phone=phone,user=None,debug=debug)

    else:
        ## Default page display
        return render_template('index.html',update=False,debug=debug)


@app.route('/admin/', methods=['GET', 'POST'])
def options():
    return render_template('admin.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404