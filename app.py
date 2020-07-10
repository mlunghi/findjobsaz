import json
import os
import _io
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
from flask_mail import Mail, Message

import databaseSetup
import dbManage
from users import User

client = MongoClient('localhost', port=27017)

db = client['mainDB']
feed = db["feed"]

app = Flask(__name__)
app.secret_key = os.urandom(24)


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME" : '',
    "MAIL_PASSWORD" : ''}

app.config.update(mail_settings)
mail = Mail(app)

Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # route or function where login occurs...


@login_manager.user_loader
@app.route('/jobRegistration', methods=['POST'])
def jobRegistration():
    title = request.form['title']
    description = request.form['description']
    location = request.form['location']
    type = request.form['typeoptions']
    toAdd = {
        "title": title,
        "description": description,
        "name": current_user.getName(),
        "email": current_user.getEmail(),
        "location" : location,
        "type" : type,
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
    return(render_template("index.html", user=current_user))

@app.route('/newpost')
@login_required
def newPost():
    return render_template("new-post.html")

@app.route('/register', methods=['GET', 'POST'])
def register():

    # force logout
    # logout_user()
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

@app.route("/jobs")
def jobs():
    all_feed = feed.find({})
    result = []
    for i in range(all_feed.count()):
        result.append(all_feed[i])
    return(render_template("job_listing.html", posts=result))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/postjob')
def postjob():
    return render_template('postjob.html')

@app.route('/jobdescription')
def singlejob():
    id = request.args.get('id')
    selected_job = feed.find_one({"_id" : ObjectId(id)})
    return render_template('job_description.html', selectedinfo=selected_job)


@app.route('/submitApplication', methods=['POST', 'GET'])
def submitApplication():
    global mail
    messageToHiringManager = request.form['message']
    experience = request.form['experience']
    salary = request.form['salary']
    skills = request.form['skills']
    resume = request.files["resume"]
    education = request.form['education']
    message = "You received a new job application! \n\n Message to the hiring manager: " + messageToHiringManager + "\n\n Highest Level of Completed Education: " + education + "\n Years of Exeperience: " + experience + "\n Expected Monthly Salary: " + salary + "\n Skills: " + skills +"\n\n Find the Resume attatched below!"
    toUs = Message("Job Application",
                   sender="testingjobmatch@gmail.com",
                   recipients=["matteo_lunghi@brown.edu", "namikmuduroglu@gmail.com", "aliyev.fuad.99@gmail.com"],
                   body=message)
    toUs.attach("resume.pdf", 'pdf/text', resume.read())
    mail.send(toUs)
    return render_template('application_submitted.html')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
