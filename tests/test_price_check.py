from app.services import check_price
from app.db.database import SessionLocal
from app.models.product import Product
from app.models.price_history import PriceHistory


def test_price_check():
    session = SessionLocal()

    try:
        product = Product(
            name="Test Product",
            url="https://example.com/test-product",
            target_price=70.00,
            current_price=75.00,
            available=True,
            image_url=None,
        )

        session.add(product)
        session.commit()
        session.refresh(product)

        initial_history = PriceHistory(
            product_id=product.id,
            price=75.00,
            available=True,
        )

        session.add(initial_history)
        session.commit()

        result = check_price(
            product_id=product.id,
            new_price=69.99,
            available=True,
            product_name="Test Product",
            target_price=70.00,
        )

        assert result["new_price"] == 69.99
        assert result["previous_price"] == 75.00
        assert result["difference"] == -5.01
        assert result["price_dropped"] is True

    finally:
        session.query(PriceHistory).filter(
            PriceHistory.product_id == product.id
        ).delete()

        session.query(Product).filter(
            Product.id == product.id
        ).delete()

        session.commit()
        session.close()


if __name__ == "__main__":
    test_price_check()
    print("Price check test passed!")
