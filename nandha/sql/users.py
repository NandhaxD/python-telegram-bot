from nandha.sql import SESSION, BASE
from sqlalchemy import Column, Integer
import threading

class Users(BASE):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    
    def __init__(self, user_id):
         self.user_id = user_id

# Create the table if it doesn't exist
Users.__table__.create(checkfirst=True)

# Thread-safe lock for database operations
INSERTION_LOCK = threading.RLock()

def add_user(user_id):
    with INSERTION_LOCK:
        user = SESSION.query(Users).get(user_id)
        if not user:
           user = Users(user_id=user_id)
           SESSION.add(user)
           SESSION.commit()

def remove_user(user_id):
    with INSERTION_LOCK:
        user = SESSION.query(Users).get(user_id)
        if user:
            SESSION.delete(user)
            SESSION.commit()

def get_all_users():
    try:
        users = SESSION.query(Users.user_id).all()
        return [user.user_id for user in users]
    finally:
        SESSION.close()
