from app.config.mysql_config import connectToMySQL

DATABASE = 'subscriptions_schema'


class Subscriber:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.magazine_id = data['magazine_id']
    
    def __repr__(self):
        return f'<Subscriber: {self.id}>'

    # create a subscriber
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO subscribers (user_id, magazine_id) VALUES (%(user_id)s, %(magazine_id)s);'
        subscriber_id = connectToMySQL(DATABASE).query_db(query, data)
        return subscriber_id

    # find all subscribers (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from subscribers;'
        results = connectToMySQL(DATABASE).query_db(query)
        subscribers = []
        for result in results:
            subscribers.append(Subscriber(result))
        return subscribers

    # find one subscriber by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from subscribers WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        subscriber = Subscriber(results[0])
        return subscriber

    # update one subscriber by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE subscribers SET user_id = %(user_id)s, magazine_id = %(magazine_id)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one subscriber by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM subscribers WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True
