import psycopg2
from psycopg2 import OperationalError, errors
import hashlib

class User:
    def __init__(self, username="", password="", _id=-1):
        self._id = _id
        self.username = username
        self._hashed_password = self._hash_password(password)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    @hashed_password.setter
    def hashed_password(self, password):
        self._hashed_password = self._hash_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                     VALUES(%s, %s) RETURNING id;"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            # Update
            sql = """UPDATE users SET username=%s, hashed_password=%s WHERE id=%s;"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s;"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            user_id, username, hashed_password = data
            loaded_user = User(username, hashed_password, user_id)
            return loaded_user
        return None



class Message:
    def __init__(self, from_id, to_id, text, _id=-1, creation_date=None):
        self._id = _id
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text)
                     VALUES(%s, %s, %s) RETURNING id, creation_date;"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self.creation_date = cursor.fetchone()
            return True

    @staticmethod
    def load_all_messages(cursor, user_id=None):
        if user_id:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s;"
            cursor.execute(sql, (user_id,))
        else:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages;"
            cursor.execute(sql)
        messages = []
        for data in cursor.fetchall():
            message_id, from_id, to_id, text, creation_date = data
            loaded_message = Message(from_id, to_id, text, message_id, creation_date)
            messages.append(loaded_message)
        return messages


@staticmethod
def load_user_by_id(cursor, user_id):
    sql = "SELECT id, username, hashed_password FROM users WHERE id=%s;"
    cursor.execute(sql, (user_id,))
    data = cursor.fetchone()
    if data:
        user_id, username, hashed_password = data
        loaded_user = User(username, hashed_password, user_id)
        return loaded_user
    return None

@staticmethod
def load_all_users(cursor):
    sql = "SELECT id, username, hashed_password FROM users;"
    cursor.execute(sql)
    users = []
    for data in cursor.fetchall():
        user_id, username, hashed_password = data
        loaded_user = User(username, hashed_password, user_id)
        users.append(loaded_user)
    return users

def delete(self, cursor):
    if self._id != -1:
        sql = "DELETE FROM users WHERE id=%s;"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True
    return False



@staticmethod
def load_message_by_id(cursor, message_id):
    sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE id=%s;"
    cursor.execute(sql, (message_id,))
    data = cursor.fetchone()
    if data:
        message_id, from_id, to_id, text, creation_date = data
        loaded_message = Message(from_id, to_id, text, message_id, creation_date)
        return loaded_message
    return None

@staticmethod
def load_messages_by_user_id(cursor, user_id):
    sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE from_id=%s OR to_id=%s;"
    cursor.execute(sql, (user_id, user_id))
    messages = []
    for data in cursor.fetchall():
        message_id, from_id, to_id, text, creation_date = data
        loaded_message = Message(from_id, to_id, text, message_id, creation_date)
        messages.append(loaded_message)
    return messages
