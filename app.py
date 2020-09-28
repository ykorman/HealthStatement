from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/',methods=('GET', 'POST'))
def main():
    if request.method == 'POST':
        print('got:' + request.form['child_name'])
    return render_template('index.html')