import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
load_dotenv()
app.secret_key = os.environ.get('SECRET_KEY')