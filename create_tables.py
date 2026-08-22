from app.db.database import Base, engine

# Import the Product model so SQLAlchemy knows about the products table
from app.models.product import Product

# Import the PriceHistory model so SQLAlchemy knows about the price_history table
from app.models.price_history import PriceHistory


def create_tables():
    # Create all tables defined by the SQLAlchemy models
    Base.metadata.create_all(bind=engine)


# Run the table creation function when this file is executed directly
if __name__ == "__main__":
    create_tables()

    # Confirm that the tables were created successfully
    print("Database tables created successfully!")