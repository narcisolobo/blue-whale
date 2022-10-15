from pprint import pprint
from app.config.mysql_config import connectToMySQL
from app.models import user
from app import flash, session

DATABASE = 'subscriptions_schema'


class Magazine:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = data['creator']
        self.subscribers = []
    
    def __repr__(self):
        return f'<Magazine: {self.title}>'
    
    @staticmethod
    def validate_magazine(form):
        is_valid = True
        if len(form['title']) < 5:
            flash('Title must be at least two characters.', 'title')
            is_valid = False
        if len(form['description']) < 10:
            flash('Description must be at least ten characters.', 'description')
            is_valid = False
        return is_valid

    # create a magazine
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO magazines (user_id, title, description) VALUES (%(user_id)s, %(title)s, %(description)s);'
        magazine_id = connectToMySQL(DATABASE).query_db(query, data)
        return magazine_id

    # find all magazines with subscribers
    @classmethod
    def find_all_with_subscribers(cls, data):
        query = 'SELECT id from magazines;'
        results = connectToMySQL(DATABASE).query_db(query)
        magazines = []
        for result in results:
            mag_data = {
                'id': result['id'],
                'logged_user': data['logged_user']
            }
            magazine = Magazine.find_by_id_with_subscribers(mag_data)
            magazines.append(magazine)
        return magazines

    # find one magazine by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from magazines WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        creator_data = {
            'id': results[0]['user_id']
        }
        creator = user.User.find_by_id(creator_data)
        magazine_data = {
            'id': results[0]['id'],
            'user_id': results[0]['user_id'],
            'species': results[0]['species'],
            'location': results[0]['location'],
            'reason': results[0]['reason'],
            'planted_at': results[0]['planted_at'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'creator': creator,
        }
        magazine = Magazine(magazine_data)
        return magazine

    # find one magazine by id with subscribers
    @classmethod
    def find_by_id_with_subscribers(cls, data):
        query = 'SELECT * from magazines LEFT JOIN subscribers ON magazines.id = subscribers.magazine_id LEFT JOIN users ON magazines.user_id = users.id WHERE magazines.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        creator_data = {
            'id': results[0]['user_id']
        }
        creator = user.User.find_by_id(creator_data)
        magazine_data = {
            'id': results[0]['id'],
            'user_id': results[0]['user_id'],
            'title': results[0]['title'],
            'description': results[0]['description'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'creator': creator,
        }
        magazine = Magazine(magazine_data)
        logged_user = data['logged_user']
        for result in results:
            if result['subscribers.user_id']:
                if result['subscribers.user_id'] == logged_user.id:
                    magazine.subscribers.append(logged_user)
                else:
                    user_data = {
                        'id': result['subscribers.user_id']
                    }
                    subscriber = user.User.find_by_id(user_data)
                    magazine.subscribers.append(subscriber)
        return magazine
    
    # update one magazine by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE magazines SET title = %(title)s, description = %(description)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one magazine by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM magazines WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

# Error Code: 1451. Cannot delete or update a parent row: a foreign key constraint fails (`abortrary_schema`.`visitors`, CONSTRAINT `fk_visitors_magazines1` FOREIGN KEY (`magazine_id`) REFERENCES `magazines` (`id`))
