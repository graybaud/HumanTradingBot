import unittest
from unittest.mock import MagicMock
from APIClient.ResponseHandler import ResponseHandler

class TestResponseHandler(unittest.TestCase):

    def test_handle_success(self):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"result": "success"}

        result = ResponseHandler.handle(response)

        self.assertEqual(result, ({"result": "success"}, "success", None))

    def test_handle_too_many_requests(self):
        response = MagicMock()
        response.status_code = 429
        response.headers = {"Retry-After": "5"}

        result = ResponseHandler.handle(response)

        self.assertEqual(result, (None, "retry", 5))

    def test_handle_ip_banned(self):
        response = MagicMock()
        response.status_code = 418
        response.headers = {"Retry-After": "60"}

        result = ResponseHandler.handle(response)

        self.assertEqual(result, (None, "ip_banned", 60))

    def test_handle_waf_limit_violation(self):
        response = MagicMock()
        response.status_code = 403

        result = ResponseHandler.handle(response)

        self.assertEqual(result, (None, "error", "WAF Limit violation"))

    def test_handle_partial_success(self):
        response = MagicMock()
        response.status_code = 409
        response.json.return_value = {"message": "Partial success"}

        result, status, _ = ResponseHandler.handle(response)

        self.assertEqual(result, {"partial_success": True, "message": "Partial success"})
        self.assertEqual(status, "partial_success")  # Vérifie le statut

    def test_handle_client_error(self):
        response = MagicMock()
        response.status_code = 400
        response.json.return_value = {"code": -1121, "msg": "Invalid symbol"}

        result = ResponseHandler.handle(response)

        self.assertEqual(result, (None, "error", "Invalid symbol: Invalid symbol"))

    def test_handle_unexpected_response(self):
        response = MagicMock()
        response.status_code = 999
        response.text = "Unexpected error"

        result = ResponseHandler.handle(response)

        self.assertEqual(result, (None, "error", "Unexpected response. Status: 999, Response: Unexpected error"))

if __name__ == '__main__':
    unittest.main()
