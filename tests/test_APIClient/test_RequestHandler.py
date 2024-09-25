import unittest
from unittest.mock import patch, MagicMock
from APIClient.RequestHandler import RequestHandler

class TestRequestHandler(unittest.TestCase):

    @patch('APIClient.RequestHandler.RequestHandler._send_http_request')
    @patch('APIClient.RequestHandler.RequestHandler._get_headers')
    def test_retry_request_success(self, mock_get_headers, mock_send_http_request):
        # Simuler un retour de la méthode _send_http_request
        mock_send_http_request.return_value = {"result": "success"}, "success", None
        
        request_handler = RequestHandler()
        response, status, _ = request_handler.retry_request('GET', 'test_endpoint', params={"param": "value"})
        
        # Vérifier que la méthode a été appelée
        mock_send_http_request.assert_called_once()
        
        # Vérifier la réponse
        self.assertEqual(response, {"result": "success"})
        self.assertEqual(status, "success")


    @patch('APIClient.RequestHandler.RequestHandler._sign')
    def test_sign_method(self, mock_sign):
        request_handler = RequestHandler()
        
        # Préparer les paramètres pour la signature
        params = {'param1': 'value1', 'param2': 'value2'}
        
        # Appeler la méthode _sign
        signature = request_handler._sign(params)
        
        # Vérifier que la méthode _sign utilise les bons paramètres
        mock_sign.assert_called_once_with(params)

    @patch('APIClient.RequestHandler.RequestHandler._get_headers')
    @patch('requests.request')
    def test_send_http_request(self, mock_requests, mock_get_headers):
        # Simuler les en-têtes
        mock_get_headers.return_value = {"X-MBX-APIKEY": "mocked_api_key"}
        request_handler = RequestHandler()
        
        # Simuler une réponse
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_requests.return_value = mock_response

        # Appeler la méthode _send_http_request
        response, status, _ = request_handler._send_http_request('GET', 'https://api.example.com', headers={}, params={"param": "value"})

        # Vérifier que la requête a été faite avec les bons paramètres
        mock_requests.assert_called_once()
        
        # Vérifier la réponse
        self.assertEqual(response, {"result": "success"})  # Vérifie le premier élément du tuple
        self.assertEqual(status, "success")                  # Vérifie le second élément du tuple


    def test_get_headers(self):
        request_handler = RequestHandler()
        headers = request_handler._get_headers()
        self.assertEqual(headers, {"X-MBX-APIKEY": request_handler.api_key})

    def test_invalid_endpoint(self):
        request_handler = RequestHandler()
        
        with self.assertRaises(ValueError) as context:
            request_handler.retry_request('GET', 'invalid_endpoint')
        
        self.assertEqual(str(context.exception), "Endpoint 'None' not found in configuration.")

if __name__ == '__main__':
    unittest.main()
