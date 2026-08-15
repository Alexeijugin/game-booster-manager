import pytest

from models.order import Order


@pytest.mark.parametrize(
    "price, hours, commission_percent, expected",
    [
        (1000, 2.5, 10, 100),
        (950, 3, 10, 95),
        (1500, 4, 15, 225),
        (700, 2, 0, 0),
        (1000, 2, 100, 1000),
    ],
)
def test_calculate_commission(price, hours, commission_percent, expected):
    order = Order(price, hours, commission_percent)

    assert order.calculate_commission() == expected


@pytest.mark.parametrize(
    "price, hours, commission_percent, expected_error",
    [
        (1000, 0, 10, "Часов должно быть больше чем 0"),
        (-100, 1, 10, "Цена должна быть больше чем 0"),
        (100, 1, -10, "Комиссия должна быть от 0 до 100"),
        (100, 1, -0.1, "Комиссия должна быть от 0 до 100"),
        (100, 1, 100.1, "Комиссия должна быть от 0 до 100"),
    ],
)
def test_order_invalid_data(
        price,
        hours,
        commission_percent,
        expected_error,
):
    with pytest.raises(ValueError, match=expected_error):
        Order(price, hours, commission_percent)


@pytest.mark.parametrize(
    "price, hours, commission_percent, expected_profit, expected_profit_per_hour",
    [
        (1000, 2.5, 10, 900, 360),
        (950, 3, 10, 855, 285),
        (1500, 4, 15, 1275, 318.75),
        (700, 2, 0, 700, 350),
    ],
)
def test_calculate_profit(price, hours, commission_percent, expected_profit, expected_profit_per_hour):
    order = Order(price, hours, commission_percent)

    profit, profit_for_hour = order.calculate_profit()

    assert profit == expected_profit
    assert profit_for_hour == pytest.approx(expected_profit_per_hour)


