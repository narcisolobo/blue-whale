from pprint import pprint
from app.config.mysql_config import connectToMySQL
from app.models import magazine
from app import flash
import re

DATABASE = 'subscriptions_schema'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.magazines = []
    
    @staticmethod
    def validate_registration(form):
        is_valid = True
        if len(form['first_name']) < 2:
            flash('First name must be at least two characters.', 'first_name')
            is_valid = False
        if len(form['last_name']) < 2:
            flash('Last name must be at least two characters.', 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('Please enter a valid email.', 'email')
            is_valid = False
        if len(form['password']) < 8:
            flash('Password must be at least eight characters.', 'password')
            is_valid = False
        else:
            if form['password'] != form['confirm_password']:
                flash('Passwords must match.', 'confirm_password')
                is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            flash('Please enter a valid email.', 'log_email')
            is_valid = False
        if len(form['password']) < 8:
            flash('Password must be at least eight characters.', 'log_password')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update(form):
        is_valid = True
        if len(form['first_name']) < 2:
            flash('First name must be at least two characters.', 'first_name')
            is_valid = False
        if len(form['last_name']) < 2:
            flash('Last name must be at least two characters.', 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('Please enter a valid email.', 'email')
            is_valid = False
        return is_valid
    
    @classmethod
    def find_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return User(results[0])
        return None
    
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return User(results[0])
        return None

    @classmethod
    def find_by_id_with_magazines(cls, data):
        query = 'SELECT * FROM users LEFT JOIN magazines ON users.id = magazines.user_id WHERE users.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        creator = User(results[0])
        if results[0]['user_id']:
            for result in results:
                magazine_data = {
                    'id': result['magazines.id'],
                    'logged_user': data['logged_user']
                }
                mag = magazine.Magazine.find_by_id_with_subscribers(magazine_data)
                creator.magazines.append(mag)
        return creator
    
    @classmethod
    def save(cls, data):
        query = 'INSERT into users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id
    
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True