import unittest
from unittest.mock import patch, MagicMock

from payment_service import PaymentService, PaymentGateway


class TestPaymentService(unittest.TestCase):
    def setUp(self):
        self.mock_payment_gateway = MagicMock()
        self.payment_service = PaymentService(self.mock_payment_gateway)

    def test_payment_success(self):
        # Arrange
        self.mock_payment_gateway.make_payment.return_value = True

        # Act
        result = self.payment_service.make_payment(100)

        # Assert
        self.assertTrue(result)
        self.mock_payment_gateway.make_payment.assert_called_once_with(100)

    def test_payment_failure(self):
        # Arrange
        self.mock_payment_gateway.make_payment.return_value = False

        # Act
        result = self.payment_service.make_payment(100)

        # Assert
        self.assertFalse(result)
        self.mock_payment_gateway.make_payment.assert_called_once_with(100)

    def test_payment_negative_amount(self):
        # Arrange
        amount = -100

        # Assert
        with self.assertRaises(ValueError):
            # Act
            self.payment_service.make_payment(amount)

        self.mock_payment_gateway.make_payment.assert_not_called()


if __name__ == "__main__":
    unittest.main()