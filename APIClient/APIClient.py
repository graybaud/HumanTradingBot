from APIClient.RequestHandler import RequestHandler
from ParameterValidator.ParameterValidator import ParameterValidator
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.request_handler = RequestHandler()

    def test_new_order(self, symbol, side, quantity, price):
        """Test new order endpoint (TRADE)."""
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": quantity,
            "price": price
        }
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('POST', 'new_order_test', params=params)

    def query_order(self, symbol, orderId):
        """Query an order's status (USER_DATA)."""
        params = {"symbol": symbol, "orderId": orderId}
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('GET', 'query_order', params=params)

    def cancel_order(self, symbol, orderId):
        """Cancel an active order (TRADE)."""
        params = {"symbol": symbol, "orderId": orderId}
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('DELETE', 'cancel_order', params=params)

    def cancel_all_orders(self, symbol):
        """Cancel all open orders on a symbol (TRADE)."""
        params = {"symbol": symbol}
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('DELETE', 'cancel_all_orders', params=params)

    def cancel_replace_order(self, symbol, cancelOrderId, new_order_params):
        """Cancel an existing order and place a new one (TRADE)."""
        ParameterValidator.validate_APIClient_params(**new_order_params)
        params = {
            "symbol": symbol,
            "cancelOrderId": cancelOrderId,
            **new_order_params
        }
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('POST', 'cancel_replace_order', params=params)

    def get_open_orders(self, symbol=None):
        """Get all open orders on a symbol (USER_DATA)."""
        params = {}
        if symbol:
            params['symbol'] = symbol
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('GET', 'open_orders', params=params)

    def get_order_history(self, symbol):
        """Get all account orders; active, canceled, or filled (USER_DATA)."""
        params = {"symbol": symbol}
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('GET', 'order_history', params=params)

    def place_oco_order(self, symbol, side, quantity, price, stopPrice):
        """Send a new OCO order (TRADE)."""
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "stopPrice": stopPrice
        }
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('POST', 'new_oco_order', params=params)

    def cancel_order_list(self, order_list_id):
        """Cancel an entire order list (TRADE)."""
        params = {"orderListId": order_list_id}
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('DELETE', 'cancel_order_list', params=params)

    def get_order_list(self, order_list_id):
        """Retrieve a specific order list (USER_DATA)."""
        params = {"orderListId": order_list_id}
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('GET', 'get_order_list', params=params)

    def get_all_order_lists(self, symbol=None):
        """Retrieve all order lists (USER_DATA)."""
        params = {}
        if symbol:
            params['symbol'] = symbol
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('GET', 'all_order_lists', params=params)

    def start_user_data_stream(self):
        """Start a new user data stream (USER_STREAM)."""
        return self.request_handler.retry_request('POST', 'start_user_data_stream')

    def keepalive_user_data_stream(self, listenKey):
        """Keepalive a user data stream (USER_STREAM)."""
        params = {"listenKey": listenKey}
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('PUT', 'keepalive_user_data_stream', params=params)

    def close_user_data_stream(self, listenKey):
        """Close a user data stream (USER_STREAM)."""
        params = {"listenKey": listenKey}
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('DELETE', 'close_user_data_stream', params=params)

    def get_account_info(self):
        """Get current account information (USER_DATA)."""
        return self.request_handler.retry_request('GET', 'account_info')

    def cancel_order_using_sor(self, symbol, side, quantity, price):
        """Cancel an order using smart order routing (SOR) (TRADE)."""
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price
        }
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('POST', 'cancel_sor_order', params=params)

    def test_new_order_using_sor(self, symbol, side, quantity, price):
        """Test new order using smart order routing (SOR) (TRADE)."""
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": quantity,
            "price": price
        }
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('POST', 'test_sor_order', params=params)

    def new_order_list_oto(self, symbol, side, quantity, price, stopPrice):
        """Create a new OTO order (TRADE)."""
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "stopPrice": stopPrice
        }
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('POST', 'new_oto_order', params=params)

    def new_order_list_otoco(self, symbol, side, quantity, price, stopPrice, stopLimitPrice):
        """Create a new OTOCO order (TRADE)."""
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "stopPrice": stopPrice,
            "stopLimitPrice": stopLimitPrice
        }
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('POST', 'new_otoco_order', params=params)

    def get_account_trade_list(self, symbol):
        """Get trades for a specific account and symbol (USER_DATA)."""
        params = {"symbol": symbol}
        ParameterValidator.validate_APIClient_params(**params)
        return self.request_handler.retry_request('GET', 'account_trade_list', params=params)

    def query_unfilled_order_count(self):
        """Query unfilled order count for all intervals (USER_DATA)."""
        return self.request_handler.retry_request('GET', 'unfilled_order_count')

    def query_prevented_matches(self):
        """Query prevented matches (USER_DATA)."""
        return self.request_handler.retry_request('GET', 'prevented_matches')

    def query_allocations(self):
        """Query allocations resulting from SOR order placement (USER_DATA)."""
        return self.request_handler.retry_request('GET', 'allocations')

    def query_commission_rates(self):
        """Query current account commission rates (USER_DATA)."""
        return self.request_handler.retry_request('GET', 'commission_rates')
