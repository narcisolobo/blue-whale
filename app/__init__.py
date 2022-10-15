import os
from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.environ.get('SECRET_KEY')