import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

import stripe
from flask_mail import Mail, Message

app = Flask(__name__)

# define routes here

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def index2():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    return render_template('job_listing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/postjob')
def postjob():
    return render_template('postjob.html')

@app.route('/singlejob')
def singlejob():
    return render_template('job_details.html')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
