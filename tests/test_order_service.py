from unittest.mock import patch
import pytest
from services.order_service import create_order_payment


def test_create_order_payment():
    with patch(
            "services.order_service.process_payment",
            return_value="Тестовая оплата",
    ) as mock_payment:

        result = create_order_payment(1000)

    mock_payment.assert_called_once_with(1000)

    assert result == "Тестовая оплата"



def test_create_order_payment_payment_error():
    with patch(
        "services.order_service.process_payment",
        side_effect=ValueError("Ошибка оплаты"),
    ):
        with pytest.raises(ValueError, match="Ошибка оплаты"):
            create_order_payment(1000)