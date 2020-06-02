import json
import os
from datetime import datetime

from bson.objectid import ObjectId
from flask import (Flask, Response, flash, redirect, render_template, request,
                   url_for)
from flask_bootstrap import Bootstrap
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

import databaseSetup
import dbManage
from users import User

client = MongoClient('localhost', port=27017)

db = client['mainDB']

app = Flask(__name__)

app.config['SECRET_KEY'] = "blah vlah"

Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # route or function where login occurs...

@app.route('/jobRegistration', methods=['POST'])
def jobRegistration():
    title = request.form['title']
    description = request.form['description']
    toAdd = {
        "title": title,
        "description": description
    }
    dbManage.addTofeed(toAdd)
    return redirect("/jobs")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.login_manager.unauthorized_handler
def unauth_handler():
    return (render_template("error.html", user=current_user))


@app.route('/', methods=['GET'])
def home():
    print(current_user.is_authenticated)
    return(render_template("index.html", user=current_user))

@app.route('/newpost')
@login_required
def newPost():
    return render_template("new-post.html")

@app.route('/register', methods=['GET', 'POST'])
def register():

    # force logout
    # logout_user()
    print("hello")
    print(request.form)
    email = request.form['email']
    password = request.form['password']
    location = request.form['ZipCode']
    user = User(email=email, location=location)
    user.password = password  # this calls the hash setter
    try:
        user.tomongo()
        return Response(json.dumps({'success': True}), 200, {'ContentType': 'application/json'})

    except Exception as e:
        print(e)
        return Response(json.dumps({'success': False}), 500, {'ContentType': 'application/json'})


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form['email']
    print(email)
    password = request.form['password']
    print(password)
    user = User.query(email)
    if(user is not None and user.verify_password(password)):
        login_user(user)
        return Response(json.dumps({'success': True}), 200, {'ContentType': 'application/json'})
    else:
        return Response(json.dumps({'success': False}), 500, {'ContentType': 'application/json'})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect("/")

## Paths for NavBar defined Here
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
