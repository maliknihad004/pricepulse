
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Load the test environment
load_dotenv(".env.test")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env.test")


# Create a database engine for testing
engine = create_engine(DATABASE_URL)


def test_database_connection():
    # Open a connection to the PricePulse PostgreSQL database
    with engine.connect() as connection:
        # Execute a simple query to verify that PostgreSQL is responding
        result = connection.execute(text("SELECT 1"))

        # Retrieve the value returned by PostgreSQL
        value = result.scalar()

        # Verify that PostgreSQL returned the expected value
        assert value == 1


# Run the connection test when this file is executed directly
if __name__ == "__main__":
    test_database_connection()

    print("Database connection successful!")
