from nandha.sql import SESSION, BASE
from sqlalchemy import Column, BigInteger
import threading

class Chats(BASE):
    __tablename__ = 'chats'
    chat_id = Column(BigInteger, primary_key=True)
    
    def __init__(self, chat_id):
         self.chat_id = chat_id

# Create the table if it doesn't exist
Chats.__table__.create(checkfirst=True)

# Thread-safe lock for database operations
INSERTION_LOCK = threading.RLock()

def add_chat(chat_id):
    with INSERTION_LOCK:
        try:
            chat = SESSION.query(Chats).get(chat_id)
            if not chat:
                chat = Chats(chat_id=chat_id)
                SESSION.add(chat)
                SESSION.commit()
        except Exception as e:
            SESSION.rollback()
            print(f"Error adding chat: {e}")

def remove_chat(chat_id):
    with INSERTION_LOCK:
        try:
            chat = SESSION.query(Chats).get(chat_id)
            if chat:
                SESSION.delete(chat)
                SESSION.commit()
        except Exception as e:
            SESSION.rollback()
            print(f"Error removing chat: {e}")

def get_all_chats():
    try:
        return [chat[0] for chat in SESSION.query(Chats.chat_id).all()]
    except Exception as e:
        print(f"Error getting all chats: {e}")
        return []
