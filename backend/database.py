import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base, User, Book


load_dotenv()

DB_HOST = os.environ["HOST_NAME"]
DB_USER = os.environ["USER_NAME"]
DB_PASSWORD = os.environ["PASSWORD"]
DB_PORT = os.environ["PORT"]
DB_NAME = os.environ["DB_NAME"]

database_url = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

def insert_db(items):
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=280,
    )

    with Session(engine) as session:

        session.add_all(items)
        session.commit()
