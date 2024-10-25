from HumanTradingBot.communication.api_client import APIClient
from HumanTradingBot.validator.parameter_validator import ParameterValidator

class GeneralEndpoint(APIClient):
    def __init__(self):
        super().__init__()  # Inherits request_handler, retry_manager, and time_offset
    
    def ping(self):
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', 'ping')

    def get_server_time(self):
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', 'time')

    def get_exchangeInfo(self, symbol=None, symbols=None, permissions=None):
        params = {}
        if symbol:
            params["symbol"] = symbol
        if symbols:
            params["symbols"] = str(symbols)
        if permissions:
            params["permissions"] = str(permissions)
        ParameterValidator.validate_APIClient_params(**params)
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', 'exchangeInfo', params=params)
