import os
from datetime import datetime

import numpy as np
import pymongo
import requests
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
feed = db["feed"]
users = db["users"]


def addTofeed(toAdd):
    feed.insert_one(toAdd)
