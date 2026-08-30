from app.services import check_target_price


def test_target_price_not_reached():
    current_price = 79.99
    target_price = 70.00

    result = check_target_price(
        current_price=current_price,
        target_price=target_price,
    )

    assert result is False


def test_target_price_reached():
    current_price = 69.99
    target_price = 70.00

    result = check_target_price(
        current_price=current_price,
        target_price=target_price,
    )

    assert result is True