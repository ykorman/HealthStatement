from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
from pdfmerge import gen_filled_form
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/',methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        gen_filled_form(request.form)
        resp = make_response(redirect(url_for('download')))
        list(map(lambda e: resp.set_cookie(e[0], e[1]), request.form.items()))
        return resp

    return render_template('index.html', cur_date=datetime.now().strftime('%d/%m/%Y'))

@app.route('/download')
def download():
    return send_file('merged_form.pdf')
