import os
from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
from celery import Celery
from datetime import datetime
from pdfmerge import gen_filled_form
from send_mail import send_mail
import redis
import base64

app = Flask(__name__)
celery = Celery(app.name, broker=os.environ.get('REDIS_URL'))

def get_form_name(form_id):
    return 'health_statement_' + form_id + '_' + datetime.now().strftime('%d_%m_%Y' + '.pdf')

@celery.task
def send_background_mail(creds, msg):
    r = redis.from_url(os.environ.get('REDIS_URL'))
    form_data = r.get(msg['attachment'])
    with open(msg['attachment'], 'wb') as f:
        f.write(base64.b64decode(form_data))
    r.delete(msg['attachment'])
    send_mail(creds, msg)
    os.unlink(msg['attachment'])

@app.route('/',methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        gen_filled_form(request.form, get_form_name(request.form.get('child_id')))
        resp = make_response(redirect(url_for('download')))
        list(map(lambda e: resp.set_cookie(e[0], e[1]), request.form.items()))
        return resp

    return render_template('index.html', cur_date=datetime.now().strftime('%d/%m/%Y'))

@app.route('/download')
def download():
    form_name = get_form_name(request.cookies.get('child_id'))
    creds = dict()
    creds['smtp'] = os.environ.get('MAIL_SMTP')
    creds['username'] = os.environ.get('MAIL_USER')
    creds['password'] = os.environ.get('MAIL_PASSWORD')
    msg = dict()
    msg['subject'] = u'הצהרת בריאות הילד לתאריך' + ' ' + datetime.now().strftime('%d/%m/%Y')
    msg['from'] = creds['username']
    msg['attachment'] = form_name
    msg['destination'] = request.cookies.get('parent_email')
    msg['body'] = u'מצורפת הצהרת בריאות חתומה'
    with open(form_name, 'rb') as f:
        form_data = base64.b64encode(f.read())
    r = redis.from_url(os.environ.get('REDIS_URL'))
    r.set(form_name, form_data)
    send_background_mail.apply_async(args=(creds, msg))
    return send_file(form_name)
