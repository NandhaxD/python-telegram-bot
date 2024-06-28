from nandha import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Initialize the base class for the declarative model
BASE = declarative_base()

def start_session() -> scoped_session:
    """
    Start and return a scoped session with the database.
    """
    engine = create_engine(DB_URL, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    session = scoped_session(sessionmaker(bind=engine, autoflush=False))
    return session

# Create a scoped session
SESSION = start_session()
