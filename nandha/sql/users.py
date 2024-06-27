


from nandha.sql import SESSION, BASE
from sqlalchemy import Column, String, Integer

import threading

class Users(BASE):
    __tablename__ = 'users'
    user_id = Column(String(14), primary_key=True)
    
    def __init__(self, user_id):
         self.user_id = user_id



Users.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock() 




def add_user(user_id):
    with INSERTION_LOCK:
        user_id = str(user_id)
        user = SESSION.query(Users).get(user_id)
        if not user:
           user = Users(user_id)
           SESSION.add(user)
           SESSION.commit()
          

def remove_user(user_id):
    user_id = str(user_id)
    user = SESSION.query(Users).get(user_id)
    if user:
        SESSION.delete(user)
        SESSION.commit()


def get_all_users():
    try:
        return SESSION.query(Users.user_id).all()
    finally:
        SESSION.close()

        
