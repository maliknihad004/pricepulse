from app.db.database import SessionLocal
from app.models.product import Product
from app.models.price_history import PriceHistory


def create_product(name, url, target_price, current_price, available):
    # Create a new database session
    session = SessionLocal()

    try:
        # Check whether a product with this URL already exists
        existing_product = (
            session.query(Product)
            .filter(Product.url == url)
            .first()
        )

        # Return the existing product instead of creating a duplicate
        if existing_product is not None:
            return existing_product

        # Create a new Product object using the supplied information
        product = Product(
            name=name,
            url=url,
            target_price=target_price,
            current_price=current_price,
            available=available,
        )

        # Add the product to the current database transaction
        session.add(product)

        # Save the product to PostgreSQL
        session.commit()

        # Refresh the object so SQLAlchemy gets generated values such as the ID
        session.refresh(product)

        # Return the newly created product
        return product

    except Exception:
        # Cancel the transaction if something goes wrong
        session.rollback()

        # Re-raise the original error
        raise

    finally:
        # Close the database session
        session.close()


def get_product_by_url(url):
    # Create a new database session
    session = SessionLocal()

    try:
        # Search for a product whose URL matches the supplied URL
        product = (
            session.query(Product)
            .filter(Product.url == url)
            .first()
        )

        # Return the product if one was found
        return product

    finally:
        # Close the database session
        session.close()


def get_all_products():
    # Create a new database session
    session = SessionLocal()

    try:
        # Retrieve all products from the database
        products = session.query(Product).all()

        # Return the list of products
        return products

    finally:
        # Close the database session
        session.close()


def update_product_price(product_id, name, current_price, available):
    # Create a new database session
    session = SessionLocal()

    try:
        # Find the product using its database ID
        product = (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        # Check whether the product exists
        if product is None:
            return None

        # Update the product's latest name
        product.name = name

        # Update the product's latest price
        product.current_price = current_price

        # Update the product's availability status
        product.available = available

        # Save the changes to PostgreSQL
        session.commit()

        # Refresh the object with the latest database values
        session.refresh(product)

        # Return the updated product
        return product

    except Exception:
        # Roll back the transaction if something goes wrong
        session.rollback()

        # Re-raise the original error
        raise

    finally:
        # Close the database session
        session.close()


def delete_product(product_id):
    # Create a new database session
    session = SessionLocal()

    try:
        # Find the product using its database ID
        product = (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        # Check whether the product exists
        if product is None:
            return None

        # Delete the product's price history first
        session.query(PriceHistory).filter(
            PriceHistory.product_id == product_id
        ).delete()

        # Delete the product
        session.delete(product)

        # Save the changes to PostgreSQL
        session.commit()

        # Return the deleted product
        return product

    except Exception:
        # Roll back the transaction if something goes wrong
        session.rollback()

        # Re-raise the original error
        raise

    finally:
        # Close the database session
        session.close()


def update_product_target_price(product_id, target_price):
    # Create a new database session
    session = SessionLocal()

    try:
        # Find the product using its database ID
        product = (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        # Check whether the product exists
        if product is None:
            return None

        # Update the target price
        product.target_price = target_price

        # Save the change to PostgreSQL
        session.commit()

        # Refresh the object with the latest database values
        session.refresh(product)

        # Return the updated product
        return product

    except Exception:
        # Roll back the transaction if something goes wrong
        session.rollback()

        # Re-raise the original error
        raise

    finally:
        # Close the database session
        session.close()


def mark_target_alert_sent(product_id):
    # Create a new database session
    session = SessionLocal()

    try:
        # Find the product using its database ID
        product = (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        # Check whether the product exists
        if product is None:
            return None

        # Mark the target-price alert as already sent
        product.target_alert_sent = True

        # Save the change to PostgreSQL
        session.commit()

        # Refresh the product with the latest database values
        session.refresh(product)

        # Return the updated product
        return product

    except Exception:
        # Roll back the transaction if something goes wrong
        session.rollback()

        # Re-raise the original error
        raise

    finally:
        # Close the database session
        session.close()


def reset_target_alert(product_id):
    # Create a new database session
    session = SessionLocal()

    try:
        # Find the product using its database ID
        product = (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        # Check whether the product exists
        if product is None:
            return None

        # Reset the alert flag so a future target crossing can trigger an alert
        product.target_alert_sent = False

        # Save the change to PostgreSQL
        session.commit()

        # Refresh the product with the latest database values
        session.refresh(product)

        # Return the updated product
        return product

    except Exception:
        # Roll back the transaction if something goes wrong
        session.rollback()

        # Re-raise the original error
        raise

    finally:
        # Close the database session
        session.close()