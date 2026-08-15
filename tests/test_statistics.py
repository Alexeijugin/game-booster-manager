from models.order import Order
from services.statistics import calculate_statistics
import pytest

def test_calculate_statistics():
    orders = [
        Order(1000, 2.5, 10),
        Order(950, 3, 10),
        Order(1500, 4, 15),
        Order(700, 2, 0),
    ]

    total_profit, total_hours, profit_per_hour = calculate_statistics(orders)

    assert total_profit == 3730
    assert total_hours == 11.5
    assert profit_per_hour == pytest.approx(324.347826)

def test_calculate_statistics_empty_orders():
    with pytest.raises(ValueError, match="Список заказов не должен быть пустым"):
        calculate_statistics([])