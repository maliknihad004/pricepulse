from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Store the connection details needed to connect to the PricePulse PostgreSQL database
DATABASE_URL = (
    "postgresql+psycopg://"
    "pricepulse:pricepulse@localhost:5432/pricepulse"
)


# Create the SQLAlchemy engine that manages connections to PostgreSQL
engine = create_engine(DATABASE_URL)


# Create a session factory that will create database sessions when needed
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    # Base class that all PricePulse SQLAlchemy models will inherit from
    pass