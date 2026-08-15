import pytest

from services.statistics import calculate_statistics
import pytest


def test_calculate_statistics(orders):
    total_profit, total_hours, profit_per_hour = calculate_statistics(orders)

    assert total_profit == 3730
    assert total_hours == 11.5
    assert profit_per_hour == pytest.approx(324.347826)


def test_calculate_statistics_empty_orders():
    with pytest.raises(ValueError, match="Список заказов не должен быть пустым"):
        calculate_statistics([])


def test_calculate_statistics_total_hours(orders):
    _, total_hours, _ = calculate_statistics(orders)

    assert total_hours == 11.5
