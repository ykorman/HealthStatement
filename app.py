from flask import Flask, render_template, request, redirect, url_for, send_file
from pdfmerge import gen_filled_form
import os

app = Flask(__name__)

@app.route('/',methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        gen_filled_form(request.form)
        return redirect(url_for('download'))

    return render_template('index.html')

@app.route('/download')
def download():
    return send_file('merged_form.pdf')
