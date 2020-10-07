from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
import os
from datetime import datetime
from pdfmerge import gen_filled_form
from send_mail import send_mail

app = Flask(__name__)

def get_form_name():
    return 'health_statement_' + datetime.now().strftime('%d_%m_%Y' + '.pdf')

@app.route('/',methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        gen_filled_form(request.form, get_form_name())
        resp = make_response(redirect(url_for('download')))
        list(map(lambda e: resp.set_cookie(e[0], e[1]), request.form.items()))
        return resp

    return render_template('index.html', cur_date=datetime.now().strftime('%d/%m/%Y'))

@app.route('/download')
def download():
    creds = dict()
    creds['smtp'] = os.environ['MAIL_SMTP']
    creds['username'] = os.environ['MAIL_USER']
    creds['password'] = os.environ['MAIL_PASSWORD']
    msg = dict()
    msg['subject'] = u'הצהרת בריאות הילד לתאריך' + ' ' + datetime.now().strftime('%d/%m/%Y')
    msg['from'] = creds['username']
    msg['attachment'] = get_form_name()
    msg['destination'] = request.cookies.get('parent_email')
    msg['body'] = u'מצורפת הצהרת בריאות חתומה'
    send_mail(creds, msg)
    return send_file(get_form_name())
