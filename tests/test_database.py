from sqlalchemy import text

from app.db.database import engine


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

    # Confirm that the database connection was successful
    print("Database connection successful!")