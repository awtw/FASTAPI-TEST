import os

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from src.database.models import Base

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin1234")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "template_db")


def get_database_url(user, password, host, port, db_name=None):
    base_url = f"mysql+pymysql://{user}:{password}@{host}:{port}"
    return f"{base_url}/{db_name}?charset=utf8mb4" if db_name else base_url


def drop_database(url, db_name):
    try:
        with create_engine(url).connect() as connection:
            connection.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
    except OperationalError as e:
        print(f"Error dropping database: {e}")


# Function to create database if it does not exist
def create_database_if_not_exists(url, db_name):
    try:
        with create_engine(url).connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    except OperationalError as e:
        print(f"Error creating database: {e}")


def drop_all_tables(_engine=None):
    try:
        Base.metadata.drop_all(bind=_engine)
        print("All tables dropped successfully.")
    except OperationalError as e:
        print(f"Error dropping tables: {e}")


# Function to create all tables
def create_all_tables(_engine=None):
    try:
        Base.metadata.create_all(bind=_engine)
        print("All tables created successfully.")
    except OperationalError as e:
        print(f"Error creating tables: {e}")


# Construct URLs
TRIAL_URL = get_database_url(DB_USER, DB_PASS, DB_HOST, DB_PORT)
SQLALCHEMY_DATABASE_URL = get_database_url(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)

# Create the database if it doesn't exist
create_database_if_not_exists(TRIAL_URL, DB_NAME)

# Pool configuration (tunable via environment for different deployments / RDS Proxy)
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "30"))
POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "600"))  # recycle before RDS idle closes
POOL_USE_LIFO = os.getenv("DB_POOL_USE_LIFO", "true").lower() == "true"
CONNECT_TIMEOUT = int(os.getenv("DB_CONNECT_TIMEOUT", "10"))

# Create engine with connection pooling options better suited for AWS RDS Proxy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,                # validate connections (essential behind proxies)
    pool_recycle=POOL_RECYCLE,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    pool_use_lifo=POOL_USE_LIFO,
    pool_reset_on_return="rollback",
    connect_args={"connect_timeout": CONNECT_TIMEOUT}
)
# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
