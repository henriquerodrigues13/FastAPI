from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from Segunda_API.APi.models import Base
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

def init_db():

    if not database_exists(db_url):
        create_database(db_url)

    Base.metadata.create_all(bind=engine)

def get_session():
    with Session(bind=engine) as session:
        yield session


