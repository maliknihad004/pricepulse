from app.db.database import SessionLocal
from app.models.product import Product
from app.models.price_history import PriceHistory


def create_product(
    name,
    url,
    image_url,
    target_price,
    current_price,
    available,
):
    session = SessionLocal()

    try:
        # Check for duplicate URL
        existing_product = (
            session.query(Product)
            .filter(Product.url == url)
            .first()
        )

        if existing_product is not None:
            return None

        # Create product
        product = Product(
            name=name,
            url=url,
            image_url=image_url,
            target_price=target_price,
            current_price=current_price,
            available=available,
        )

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def get_product_by_url(url):
    session = SessionLocal()

    try:
        return (
            session.query(Product)
            .filter(Product.url == url)
            .first()
        )

    finally:
        session.close()


def get_product_by_id(product_id):
    session = SessionLocal()

    try:
        return (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    finally:
        session.close()


def get_all_products():
    session = SessionLocal()

    try:
        return (
            session.query(Product)
            .order_by(Product.created_at.desc())
            .all()
        )

    finally:
        session.close()


def update_product_price(
    product_id,
    name,
    image_url,
    current_price,
    available,
):
    session = SessionLocal()

    try:
        product = (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if product is None:
            return None

        product.name = name
        product.image_url = image_url
        product.current_price = current_price
        product.available = available

        session.commit()
        session.refresh(product)

        return product

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def update_product_target_price(
    product_id,
    target_price,
):
    session = SessionLocal()

    try:
        product = (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if product is None:
            return None

        product.target_price = target_price

        # Allow another alert when target price changes
        product.target_alert_sent = False

        session.commit()
        session.refresh(product)

        return product

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def delete_product(product_id):
    session = SessionLocal()

    try:
        product = (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if product is None:
            return None

        # Delete related price history first
        session.query(
            PriceHistory
        ).filter(
            PriceHistory.product_id == product_id
        ).delete()

        # Delete product
        session.delete(product)

        session.commit()

        return product

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def mark_target_alert_sent(product_id):
    session = SessionLocal()

    try:
        product = (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if product is None:
            return None

        product.target_alert_sent = True

        session.commit()
        session.refresh(product)

        return product

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def reset_target_alert(product_id):
    session = SessionLocal()

    try:
        product = (
            session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if product is None:
            return None

        product.target_alert_sent = False

        session.commit()
        session.refresh(product)

        return product

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()