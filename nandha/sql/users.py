from nandha.sql import SESSION, BASE
from sqlalchemy import Column, Integer, String, Boolean, BigInteger
import threading

class Users(BASE):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String)
    username = Column(String)
    is_bot = Column(Boolean)
    language_code = Column(String)

    def __init__(self, user_id, first_name, username, is_bot, language_code):
        self.user_id = user_id
        self.first_name = first_name
        self.username = username
        self.is_bot = is_bot
        self.language_code = language_code

# Create the table if it doesn't exist
Users.__table__.create(checkfirst=True)

# Thread-safe lock for database operations
INSERTION_LOCK = threading.RLock()


def add_user(obj):
    with INSERTION_LOCK:
        try:
            user_id = obj['id']
            user = SESSION.query(Users).get(user_id)
            if not user:
                user = Users(
                    user_id=user_id,
                    first_name=obj.get('first_name'),
                    username=obj.get('username'),
                    is_bot=obj.get('is_bot'),
                    language_code=obj.get('language_code')
                )
                SESSION.add(user)
                SESSION.commit()
                
        except Exception as e:
            SESSION.rollback()
            print(f"Error adding user: {e}")

def remove_user(user_id):
    with INSERTION_LOCK:
        try:
            user = SESSION.query(Users).get(user_id)
            if user:
                SESSION.delete(user)
                SESSION.commit()
                
        except Exception as e:
            SESSION.rollback()
            print(f"Error removing user: {e}")


def get_user_data(user_id):
    try:
        user = SESSION.query(Users).get(user_id)
        data = {}
        if user:
            data = { key: value for key, value in user.__dict__.items() if not key.startswith('_') }
        return data
    except Exception as e:
        print(f"Error getting user: {e}")
        return data




def get_all_users():
    try:
        return [user.user_id for user in SESSION.query(Users).all()]
    except Exception as e:
        print(f"Error getting all users: {e}")
        return []
