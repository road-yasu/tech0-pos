import datetime
import os

from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base, User, Book, Customer, Tax


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

connect_args = {"charset": "utf8mb4"}
if DB_HOST not in ("localhost", "127.0.0.1"):
    connect_args["ssl"] = {"check_hostname": False}

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_recycle=280,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()