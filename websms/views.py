from flask import render_template,session,redirect,url_for,request,current_app,make_response

## from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import update,select
from sqlalchemy.sql import extract,and_,or_

from websms import app
from websms.database import db
from websms.models import AlertsSubscriberData

import requests
import re
import json
import ldap
from datetime import datetime

def check_phone_number(number):
    #validate the phone number; check length and correct format, no alphas
    if len(number) == 10:
        if not re.match("04[0-9]+", number):
            return False
        return True
    else:
        return False

def check_name(name):
    #validate the supplied name; check length and correct format, no numbers or special chars
    if len(name) > 1:
        if not re.match("[A-Za-z ]+", name):
            return False
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def websms():
    debug = None
    if request.method == 'POST':
        if request.form['state-machine'] == "query":
            phone = request.form['phone-number'].strip()

            # validate the phone number and redirect to index page if no good.
            if not check_phone_number(phone):
                debug = "Incorrect phone number format, try 04[xxxxxxxx]"
                return render_template('index.html',update=False,phone=phone,user=None,debug=debug)

            # run a database search on the supplied phone number
            subscriber = AlertsSubscriberData.query.filter_by(number = phone).first()

            # if the user exists in DB then proceed to update
            if subscriber:
                if subscriber.subscriber_id == 10:
                    return render_template('index.html',update=True,phone=phone,user=subscriber,admin=True,debug=debug)
                return render_template('index.html',update=True,phone=phone,user=subscriber,debug=debug)
            # if the user not exists in DB then proceed to create user
            else:
                debug = "No user found, create new entry"
                return render_template('index.html',update=True,phone=phone,user=None,debug=debug)

        if request.form['state-machine'] == "update":
            #return request.form['submit_select']

            name = request.form['name'].strip()
            phone = request.form['phone-number'].strip()
            subscription_ok = request.form.get('subscription_active','')
            subscription_bd = request.form.get('subscription_bd','')
            subscription_br = request.form.get('subscription_br','')
            subscription_fsm = request.form.get('subscription_fsm','')
            subscription_blam = request.form.get('subscription_blam','')

            # store the form data to repopulate form before saving to DB
            tmp_data = AlertsSubscriberData(name=name,number=phone)
            subscription = ""

            if subscription_ok:
                tmp_data.active = 1
            if subscription_bd:
                subscription = subscription + "Beam Down. "
                tmp_data.alert_on_beam_down = 1
            if subscription_br:
                subscription = subscription + "Beam Up. "
                tmp_data.alert_on_beam_up = 1
            if subscription_fsm:
                subscription = subscription + "FSM. "
                tmp_data.alert_on_fsm = 1
            if subscription_blam:
                subscription = subscription + "Science Group. "
                tmp_data.alert_on_blam = 1

            # validate the phone number and redirect to index page if no good.
            if not check_phone_number(phone):
                debug = "Incorrect phone number format, try 04[xxxxxxxx]"
                return render_template('index.html',update=True,phone=phone,user=tmp_data,debug=debug)

            # validate the phone number and redirect to index page if no good.
            if not check_name(name):
                debug = "This doesn't look like a regular name, try [First Last]. Numerals or special chars are not accepted."
                return render_template('index.html',update=True,phone=phone,user=tmp_data,debug=debug)

            # the test button was selected, prepare and send test SMS
            if request.form['submit_select'] == "test":

                send_string = "Hello %s, you have requested the following Notification Services: %s" % (name, subscription)
                #dict_send = {'message': send_string, 'numbers': phone}

                #result = requests.post('http://10.6.100.199:8080?message%s%numbers=%s', data=json.dumps(dict_send))
                result = requests.post('http://10.6.100.199:8080?message=%s&numbers=%s' % (send_string,phone))
                #return send_string

                debug = "Check your phone for a txt msg. If not received after a few minutes please contact the Control Room."

                return render_template('index.html',update=True,phone=phone,user=tmp_data,debug=debug)
            else:
                #time = datetime.date().today().strftime("%Y-%m-%d %H:%M:%s")
                time = datetime.now()
                # update the user in the DB
                subscriber = AlertsSubscriberData.query.filter_by(number = phone).first()

                subscriber.name = tmp_data.name
                subscriber.number = tmp_data.number
                subscriber.alert_on_beam_down = tmp_data.alert_on_beam_down
                subscriber.alert_on_beam_up = tmp_data.alert_on_beam_up
                subscriber.alert_on_fsm = tmp_data.alert_on_fsm
                subscriber.alert_on_blam = tmp_data.alert_on_blam
                subscriber.active = tmp_data.active
                subscriber.modified = time

                db.session.commit()
                debug = "User subscription information has been updated"
                return render_template('index.html',update=False,debug=debug)

        if request.form['state-machine'] == "new":
            name = request.form['name'].strip()
            phone = request.form['phone-number'].strip()
            subscription_ok = request.form.get('subscription_active','')
            subscription_bd = request.form.get('subscription_bd','')
            subscription_br = request.form.get('subscription_br','')
            subscription_fsm = request.form.get('subscription_fsm','')
            subscription_blam = request.form.get('subscription_blam','')

            # store the form data to repopulate form before saving to DB
            tmp_data = AlertsSubscriberData(name=name,number=phone)
            subscription = ""

            if subscription_ok:
                tmp_data.active = 1
            if subscription_bd:
                subscription = subscription + "Beam Down. "
                tmp_data.alert_on_beam_down = 1
            if subscription_br:
                subscription = subscription + "Beam Up. "
                tmp_data.alert_on_beam_up = 1
            if subscription_fsm:
                subscription = subscription + "FSM. "
                tmp_data.alert_on_fsm = 1
            if subscription_blam:
                subscription = subscription + "Science Group. "
                tmp_data.alert_on_blam = 1

            # validate the phone number and redirect to index page if no good.
            if not check_phone_number(phone):
                debug = "Incorrect phone number format, try 04[xxxxxxxx]"
                return render_template('index.html',update=True,phone=phone,user=tmp_data,debug=debug)

            # validate the phone number and redirect to index page if no good.
            if not check_name(name):
                debug = "This doesn't look like a regular name, try [First Last]. Numerals or special chars are not accepted."
                return render_template('index.html',update=True,phone=phone,user=tmp_data,debug=debug)

            # the test button was selected, prepare and send test SMS
            if request.form['submit_select'] == "test":

                send_string = "Hello %s, you have requested the following Notification Services: %s" % (name, subscription)
                #dict_send = {'message': send_string, 'numbers': phone}

                #result = requests.post('http://10.6.100.199:8080?message%s%numbers=%s', data=json.dumps(dict_send))
                result = requests.post('http://10.6.100.199:8080?message=%s&numbers=%s' % (send_string,phone))
                #return send_string

                debug = "Check your phone for a txt msg. If not received after a few minutes please contact the Control Room."

                return render_template('index.html',update=True,phone=phone,user=tmp_data,debug=debug)
            else:

                time = datetime.now()
                # create the user in the DB
                tmp_data.date_added = time

                db.session.add(tmp_data)
                db.session.commit()

                debug = "User subscription information has been added to the database"
                return render_template('index.html',update=False,debug=debug)

        else:
            ## if the post request was not delivered from a form, generate error
            return render_template('404.html'), 404

    else:
        ## Default page display GET
        return render_template('index.html',update=False,debug=debug)


@app.route('/admin/', methods=['GET', 'POST'])
def options():
    if request.method == 'POST':
        message = request.form['message'].strip()
        message_group = request.form['message_group']
        message_user = request.form['message_user']
        single_phone = request.form['phone'].strip()

        if message_group == "None" and message_user == "None" and single_phone == '':
            debug = "I don't know who to send this to... Select a group or enter an individual number"
            return render_template('admin.html',debug=debug,admin=True,phone_dict=phone_list)



    phone_list = AlertsSubscriberData.query.filter_by(active = 1).order_by(AlertsSubscriberData.name).all()
    #subscriber = AlertsSubscriberData.query.filter_by(number = phone).first()
    debug = ""
    return render_template('admin.html',debug=debug,admin=True,phone_dict=phone_list)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404