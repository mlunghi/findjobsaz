import os
from datetime import datetime

import pymongo
from bson.objectid import ObjectId
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['mainDB']
users = db["users"]


class User(UserMixin):

    def __init__(self, email, location):
        self.email = email
        self._id = None
        self.password_hash = None
        self.location = location

    @property
    def password(self):
        raise AttributeError('password is write-only')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # overload for flask_login
    def get_id(self):
        return str(self._id)  # reuse MongoDB id

    def query(key):
        # pass in email or name as key
        print("reached")
        doc = users.find_one({'$or': [{'email': key}]})
        print(doc)
        if doc is None:
            return None
        u = User(email=doc['email'], location=doc['location'])
        u.password_hash = doc['password_hash']
        u._id = doc['_id']
        print(u.email)
        return u

    def get(id):
        doc = db.users.find_one({'_id': ObjectId(id)})
        if doc is None:
            return None
        u = User(email=doc['email'], location=doc['location'])
        u.password_hash = doc['password_hash']
        u._id = doc['_id']
        return u

    def tomongo(self):
        # update info in mongodb
        print("yeesssirrr")
        q = {'email': self.email,
             'password_hash': self.password_hash, 'location': self.location}

        # if _id field is there, then retrieved user
        if self._id:
            db.users.update_one({'_id': self._id}, {'$set': q})
        else:
            # create new user

            # check a user under these keys does not exist yet!
            # assert User.query(
            #     self.email) is None, 'user name {} already registered'.format(self.name)
            print(q)
            assert User.query(
                self.email) is None, 'email {} already registered'.format(self.email)
            self._id = users.insert_one(q).inserted_id
