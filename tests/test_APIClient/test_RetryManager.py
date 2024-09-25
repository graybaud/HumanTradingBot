import unittest
from unittest.mock import MagicMock, patch
from Configuration import config
from APIClient.RetryManager import RetryManager

class TestRetryManager(unittest.TestCase):

    def setUp(self):
        # Configuration mock pour les tests
        self.original_retries = config.RETRIES
        self.original_max_retry_time = config.MAX_RETRY_TIME
        config.RETRIES = 3
        config.MAX_RETRY_TIME = 10

        self.retry_manager = RetryManager()

    def tearDown(self):
        # Restauration de la configuration originale
        config.RETRIES = self.original_retries
        config.MAX_RETRY_TIME = self.original_max_retry_time

    def test_execute_with_retry_success(self):
        mock_func = MagicMock(return_value="success")
        result = self.retry_manager.execute_with_retry(mock_func)

        self.assertEqual(result, "success")
        self.assertEqual(mock_func.call_count, 1)

    def test_execute_with_retry_fail_once(self):
        mock_func = MagicMock(side_effect=[Exception("Failed"), "success"])
        result = self.retry_manager.execute_with_retry(mock_func)

        self.assertEqual(result, "success")
        self.assertEqual(mock_func.call_count, 2)

    def test_execute_with_retry_fail_multiple_times(self):
        mock_func = MagicMock(side_effect=Exception("Failed"))
        with self.assertRaises(Exception) as context:
            self.retry_manager.execute_with_retry(mock_func)

        self.assertEqual(str(context.exception), "Failed")
        self.assertEqual(mock_func.call_count, 3)

    def test_execute_with_retry_max_retry_time_exceeded(self):
        mock_func = MagicMock(side_effect=Exception("Failed"))

        # Ajuster max_retry_time pour s'assurer que l'exception soit levée
        self.retry_manager.max_retry_time = 0.01  # 10 ms
        with self.assertRaises(Exception) as context:
            self.retry_manager.execute_with_retry(mock_func)

        self.assertEqual(str(context.exception), "Max retry time exceeded.")

if __name__ == '__main__':
    unittest.main()
