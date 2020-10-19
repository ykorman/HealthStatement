from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
from celery import Celery
import os
from datetime import datetime
from pdfmerge import gen_filled_form
from send_mail import send_mail

app = Flask(__name__)
celery = Celery(app.name, broker=os.environ.get('REDIS_URL'))

def get_form_name(request):
    return 'health_statement_' + request.cookies.get('child_id') + '_' + datetime.now().strftime('%d_%m_%Y' + '.pdf')

@celery.task
def send_background_mail(form_name, creds, msg):
    send_mail(creds, msg)
    os.unlink(form_name)

@app.route('/',methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        resp = make_response(redirect(url_for('download')))
        list(map(lambda e: resp.set_cookie(e[0], e[1]), request.form.items()))
        gen_filled_form(request.form, get_form_name(request))
        return resp

    return render_template('index.html', cur_date=datetime.now().strftime('%d/%m/%Y'))

@app.route('/download')
def download():
    creds = dict()
    creds['smtp'] = os.environ.get('MAIL_SMTP')
    creds['username'] = os.environ.get('MAIL_USER')
    creds['password'] = os.environ.get('MAIL_PASSWORD')
    msg = dict()
    msg['subject'] = u'הצהרת בריאות הילד לתאריך' + ' ' + datetime.now().strftime('%d/%m/%Y')
    msg['from'] = creds['username']
    msg['attachment'] = get_form_name(request)
    msg['destination'] = request.cookies.get('parent_email')
    msg['body'] = u'מצורפת הצהרת בריאות חתומה'
    send_background_mail.apply_async(args=(get_form_name(request), creds, msg))
    return send_file(get_form_name(request))
