from sqlalchemy import desc

from app.db.database import SessionLocal
from app.models.price_history import PriceHistory


def create_price_history(product_id, price, available):
    # Create a new database session
    session = SessionLocal()

    try:
        # Create a new price history record
        history = PriceHistory(
            product_id=product_id,
            price=price,
            available=available,
        )

        # Add the record to the current transaction
        session.add(history)

        # Save the record to PostgreSQL
        session.commit()

        # Refresh the object to get generated values such as its ID
        session.refresh(history)

        # Return the newly created history record
        return history

    except Exception:
        # Roll back the transaction if an error occurs
        session.rollback()

        # Re-raise the original error
        raise

    finally:
        # Close the database session
        session.close()


def get_latest_price_history(product_id):
    # Create a new database session
    session = SessionLocal()

    try:
        # Find the most recent price history record for the product
        history = (
            session.query(PriceHistory)
            .filter(PriceHistory.product_id == product_id)
            .order_by(desc(PriceHistory.checked_at))
            .first()
        )

        # Return the latest record, or None if no history exists
        return history

    finally:
        # Close the database session
        session.close()