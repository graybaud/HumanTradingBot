import unittest
from unittest.mock import patch, MagicMock
from APIClient.APIClient import APIClient

class TestAPIClient(unittest.TestCase):

    def setUp(self):
        """Initialisation de l'APIClient pour les tests"""
        self.api_client = APIClient()


    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_cancel_replace_order_success(self, mock_retry_request):
        # Simuler l'annulation réussie de l'ancien ordre
        mock_retry_request.side_effect = [
            ({"orderId": 12345}, "success", None),  # Cancel Order
            ({"orderId": 67890}, "success", None)   # New Order
        ]

        new_order_params = {
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": 1,
            "price": 50000
        }

        # Appeler la méthode cancel_replace_order
        response, status, _ = self.api_client.cancel_replace_order("BTCUSDT", 12345, new_order_params)

        # Vérifier que l'annulation est effectuée en premier
        mock_retry_request.assert_any_call('POST', 'cancel_replace_order', params={
            "symbol": "BTCUSDT",
            "cancelOrderId": 12345,
            **new_order_params
        })

        # Vérifier que le nouvel ordre est créé après l'annulation
        self.assertEqual(mock_retry_request.call_count, 1)
        self.assertEqual(status, "success")
        self.assertEqual(response['orderId'], 12345)

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_cancel_replace_order_failure(self, mock_retry_request):
        """Test de la méthode cancel_replace_order (échec de l'annulation)"""
        # Simuler l'échec de l'annulation d'ordre
        mock_retry_request.side_effect = [
            (None, "error", "Order not found"),  # Cancel Order failure
        ]

        # Appeler la méthode cancel_replace_order
        new_order_params = {
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": 1,
            "price": 50000
        }
        response, status, error = self.api_client.cancel_replace_order("BTCUSDT", 12345, new_order_params)

        # Vérifier que l'ordre n'est pas créé en cas d'échec de l'annulation
        self.assertEqual(mock_retry_request.call_count, 1)
        self.assertEqual(status, "error")
        self.assertEqual(error, "Order not found")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_test_new_order(self, mock_retry_request):
        """Test la méthode test_new_order"""
        # Setup du mock
        mock_retry_request.return_value = ({"orderId": 12345}, "success", None)

        # Appel de la méthode testée
        response, status, _ = self.api_client.test_new_order("BTCUSDT", "BUY", 1, 50000)

        # Assertions
        mock_retry_request.assert_called_once_with('POST', 'new_order_test', params={
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": 1,
            "price": 50000
        })
        self.assertEqual(status, "success")
        self.assertEqual(response['orderId'], 12345)

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_test_new_order_invalid_params(self, mock_retry_request):
        """Test la méthode test_new_order avec des paramètres invalides"""
        # Test avec un symbole invalide
        with self.assertRaises(ValueError):
            self.api_client.test_new_order("", "BUY", 1, 50000)

        # Test avec une quantité négative
        with self.assertRaises(ValueError):
            self.api_client.test_new_order("BTCUSDT", "BUY", -1, 50000)

        # Test avec un prix nul
        with self.assertRaises(ValueError):
            self.api_client.test_new_order("BTCUSDT", "BUY", 1, 0)

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_retry_request_failure(self, mock_retry_request):
        """Test la gestion d'une erreur de l'API (exemple d'échec réseau)"""
        # Simuler une exception lors de l'appel à l'API
        mock_retry_request.side_effect = Exception("Erreur réseau")

        # Tester que l'exception est bien levée par l'API client
        with self.assertRaises(Exception):
            self.api_client.test_new_order("BTCUSDT", "BUY", 1, 50000)

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_query_order_invalid_params(self, mock_retry_request):
        """Test la méthode query_order avec des paramètres invalides"""
        # Test avec un order_id invalide
        with self.assertRaises(ValueError):
            self.api_client.query_order("BTCUSDT", -1)

        # Test avec un symbole manquant
        with self.assertRaises(ValueError):
            self.api_client.query_order("", 12345)

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_query_order(self, mock_retry_request):
        """Test la méthode query_order"""
        mock_retry_request.return_value = ({"orderId": 67890}, "success", None)
        response, status, _ = self.api_client.query_order("BTCUSDT", 67890)
        mock_retry_request.assert_called_once_with('GET', 'query_order', params={"symbol": "BTCUSDT", "orderId": 67890})
        self.assertEqual(response['orderId'], 67890)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_cancel_order(self, mock_retry_request):
        """Test la méthode cancel_order"""
        mock_retry_request.return_value = ({"msg": "Order canceled"}, "success", None)
        response, status, _ = self.api_client.cancel_order("BTCUSDT", 67890)
        mock_retry_request.assert_called_once_with('DELETE', 'cancel_order', params={"symbol": "BTCUSDT", "orderId": 67890})
        self.assertEqual(response['msg'], "Order canceled")
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_cancel_all_orders(self, mock_retry_request):
        """Test la méthode cancel_all_orders"""
        mock_retry_request.return_value = ({"msg": "All orders canceled"}, "success", None)
        response, status, _ = self.api_client.cancel_all_orders("BTCUSDT")
        mock_retry_request.assert_called_once_with('DELETE', 'cancel_all_orders', params={"symbol": "BTCUSDT"})
        self.assertEqual(response['msg'], "All orders canceled")
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_cancel_replace_order(self, mock_retry_request):
        """Test la méthode cancel_replace_order"""
        mock_retry_request.return_value = ({"orderId": 99999}, "success", None)
        new_order_params = {
            "side": "BUY",
            "type": "LIMIT",
            "quantity": 1,
            "price": 50500
        }
        response, status, _ = self.api_client.cancel_replace_order("BTCUSDT", 67890, new_order_params)
        expected_params = {
            "symbol": "BTCUSDT",
            "cancelOrderId": 67890,
            **new_order_params
        }
        mock_retry_request.assert_called_once_with('POST', 'cancel_replace_order', params=expected_params)
        self.assertEqual(response['orderId'], 99999)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_get_open_orders(self, mock_retry_request):
        """Test la méthode get_open_orders sans symbole"""
        mock_retry_request.return_value = ([{"orderId": 123}], "success", None)
        response, status, _ = self.api_client.get_open_orders()
        mock_retry_request.assert_called_once_with('GET', 'open_orders', params={})
        self.assertEqual(len(response), 1)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_get_open_orders_with_symbol(self, mock_retry_request):
        """Test la méthode get_open_orders avec symbole"""
        mock_retry_request.return_value = ([{"orderId": 456}], "success", None)
        response, status, _ = self.api_client.get_open_orders("BTCUSDT")
        mock_retry_request.assert_called_once_with('GET', 'open_orders', params={"symbol": "BTCUSDT"})
        self.assertEqual(len(response), 1)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_get_order_history(self, mock_retry_request):
        """Test la méthode get_order_history"""
        mock_retry_request.return_value = ([{"orderId": 789}], "success", None)
        response, status, _ = self.api_client.get_order_history("BTCUSDT")
        mock_retry_request.assert_called_once_with('GET', 'order_history', params={"symbol": "BTCUSDT"})
        self.assertEqual(len(response), 1)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_place_oco_order(self, mock_retry_request):
        """Test la méthode place_oco_order"""
        mock_retry_request.return_value = ({"orderListId": 1122}, "success", None)
        response, status, _ = self.api_client.place_oco_order("BTCUSDT", "SELL", 1, 51000, 49500)
        expected_params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "quantity": 1,
            "price": 51000,
            "stopPrice": 49500
        }
        mock_retry_request.assert_called_once_with('POST', 'new_oco_order', params=expected_params)
        self.assertEqual(response['orderListId'], 1122)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_cancel_order_list(self, mock_retry_request):
        """Test la méthode cancel_order_list"""
        mock_retry_request.return_value = ({"msg": "Order list canceled"}, "success", None)
        response, status, _ = self.api_client.cancel_order_list(3344)
        mock_retry_request.assert_called_once_with('DELETE', 'cancel_order_list', params={"orderListId": 3344})
        self.assertEqual(response['msg'], "Order list canceled")
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_get_order_list(self, mock_retry_request):
        """Test la méthode get_order_list"""
        mock_retry_request.return_value = ({"orderListId": 3344}, "success", None)
        response, status, _ = self.api_client.get_order_list(3344)
        mock_retry_request.assert_called_once_with('GET', 'get_order_list', params={"orderListId": 3344})
        self.assertEqual(response['orderListId'], 3344)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_get_all_order_lists(self, mock_retry_request):
        """Test la méthode get_all_order_lists sans symbole"""
        mock_retry_request.return_value = ([{"orderListId": 5566}], "success", None)
        response, status, _ = self.api_client.get_all_order_lists()
        mock_retry_request.assert_called_once_with('GET', 'all_order_lists', params={})
        self.assertEqual(len(response), 1)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_get_all_order_lists_with_symbol(self, mock_retry_request):
        """Test la méthode get_all_order_lists avec symbole"""
        mock_retry_request.return_value = ([{"orderListId": 7788}], "success", None)
        response, status, _ = self.api_client.get_all_order_lists("BTCUSDT")
        mock_retry_request.assert_called_once_with('GET', 'all_order_lists', params={"symbol": "BTCUSDT"})
        self.assertEqual(len(response), 1)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_start_user_data_stream(self, mock_retry_request):
        """Test la méthode start_user_data_stream"""
        mock_retry_request.return_value = ({"listenKey": "abc123"}, "success", None)
        response, status, _ = self.api_client.start_user_data_stream()
        mock_retry_request.assert_called_once_with('POST', 'start_user_data_stream')
        self.assertEqual(response['listenKey'], "abc123")
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_keepalive_user_data_stream(self, mock_retry_request):
        """Test la méthode keepalive_user_data_stream"""
        mock_retry_request.return_value = ({"msg": "Stream kept alive"}, "success", None)
        response, status, _ = self.api_client.keepalive_user_data_stream("abc123")
        mock_retry_request.assert_called_once_with('PUT', 'keepalive_user_data_stream', params={"listenKey": "abc123"})
        self.assertEqual(response['msg'], "Stream kept alive")
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_close_user_data_stream(self, mock_retry_request):
        """Test la méthode close_user_data_stream"""
        mock_retry_request.return_value = ({"msg": "Stream closed"}, "success", None)
        response, status, _ = self.api_client.close_user_data_stream("abc123")
        mock_retry_request.assert_called_once_with('DELETE', 'close_user_data_stream', params={"listenKey": "abc123"})
        self.assertEqual(response['msg'], "Stream closed")
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_get_account_info(self, mock_retry_request):
        """Test la méthode get_account_info"""
        mock_retry_request.return_value = ({"account": "info"}, "success", None)
        response, status, _ = self.api_client.get_account_info()
        mock_retry_request.assert_called_once_with('GET', 'account_info')
        self.assertEqual(response['account'], "info")
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_cancel_order_using_sor(self, mock_retry_request):
        """Test la méthode cancel_order_using_sor"""
        mock_retry_request.return_value = ({"msg": "SOR order canceled"}, "success", None)
        response, status, _ = self.api_client.cancel_order_using_sor("BTCUSDT", "SELL", 1, 50000)
        expected_params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "quantity": 1,
            "price": 50000
        }
        mock_retry_request.assert_called_once_with('POST', 'cancel_sor_order', params=expected_params)
        self.assertEqual(response['msg'], "SOR order canceled")
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_test_new_order_using_sor(self, mock_retry_request):
        """Test la méthode test_new_order_using_sor"""
        mock_retry_request.return_value = ({"orderId": 55555}, "success", None)
        response, status, _ = self.api_client.test_new_order_using_sor("BTCUSDT", "BUY", 1, 50000)
        expected_params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": 1,
            "price": 50000
        }
        mock_retry_request.assert_called_once_with('POST', 'test_sor_order', params=expected_params)
        self.assertEqual(response['orderId'], 55555)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_new_order_list_oto(self, mock_retry_request):
        """Test la méthode new_order_list_oto"""
        mock_retry_request.return_value = ({"orderListId": 66666}, "success", None)
        response, status, _ = self.api_client.new_order_list_oto("BTCUSDT", "BUY", 1, 50000, 49000)
        expected_params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "quantity": 1,
            "price": 50000,
            "stopPrice": 49000
        }
        mock_retry_request.assert_called_once_with('POST', 'new_oto_order', params=expected_params)
        self.assertEqual(response['orderListId'], 66666)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_new_order_list_otoco(self, mock_retry_request):
        """Test la méthode new_order_list_otoco"""
        mock_retry_request.return_value = ({"orderListId": 77777}, "success", None)
        response, status, _ = self.api_client.new_order_list_otoco("BTCUSDT", "BUY", 1, 50000, 49000, 48000)
        expected_params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "quantity": 1,
            "price": 50000,
            "stopPrice": 49000,
            "stopLimitPrice": 48000
        }
        mock_retry_request.assert_called_once_with('POST', 'new_otoco_order', params=expected_params)
        self.assertEqual(response['orderListId'], 77777)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_get_account_trade_list(self, mock_retry_request):
        """Test la méthode get_account_trade_list"""
        mock_retry_request.return_value = ([{"tradeId": 88888}], "success", None)
        response, status, _ = self.api_client.get_account_trade_list("BTCUSDT")
        mock_retry_request.assert_called_once_with('GET', 'account_trade_list', params={"symbol": "BTCUSDT"})
        self.assertEqual(len(response), 1)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_query_unfilled_order_count(self, mock_retry_request):
        """Test la méthode query_unfilled_order_count"""
        mock_retry_request.return_value = ({"count": 5}, "success", None)
        response, status, _ = self.api_client.query_unfilled_order_count()
        mock_retry_request.assert_called_once_with('GET', 'unfilled_order_count')
        self.assertEqual(response['count'], 5)
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_query_prevented_matches(self, mock_retry_request):
        """Test la méthode query_prevented_matches"""
        mock_retry_request.return_value = ({"matches": []}, "success", None)
        response, status, _ = self.api_client.query_prevented_matches()
        mock_retry_request.assert_called_once_with('GET', 'prevented_matches')
        self.assertEqual(response['matches'], [])
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_query_allocations(self, mock_retry_request):
        """Test la méthode query_allocations"""
        mock_retry_request.return_value = ({"allocations": []}, "success", None)
        response, status, _ = self.api_client.query_allocations()
        mock_retry_request.assert_called_once_with('GET', 'allocations')
        self.assertEqual(response['allocations'], [])
        self.assertEqual(status, "success")

    @patch('APIClient.RequestHandler.RequestHandler.retry_request')
    def test_query_commission_rates(self, mock_retry_request):
        """Test la méthode query_commission_rates"""
        mock_retry_request.return_value = ({"makerCommission": 0.001}, "success", None)
        response, status, _ = self.api_client.query_commission_rates()
        mock_retry_request.assert_called_once_with('GET', 'commission_rates')
        self.assertEqual(response['makerCommission'], 0.001)
        self.assertEqual(status, "success")

if __name__ == '__main__':
    unittest.main()
