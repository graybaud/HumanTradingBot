from HumanTradingBot.communication.api_client import APIClient
from HumanTradingBot.validator.parameter_validator import ParameterValidator

class MarketData(APIClient):
    def __init__(self):
        super().__init__()  # Inherits request_handler, retry_manager, and time_offset

    def get_depth(self, symbol: str, limit: int = 100):
        params = {
            'symbol': symbol,
            'limit': limit
        }
        return self.request_handler.retry_request('GET', '/api/v3/depth', params=params)

    def get_aggtrades(self, symbol: str, fromId: int = None, startTime: int = None, endTime: int = None, limit: int = 500):
        params = {
            'symbol': symbol,
            'limit': limit
        }
        if fromId:
            params['fromId'] = fromId
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        ParameterValidator.validate_APIClient_params(**params)
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', '/api/v3/aggTrades', params=params)

    def get_historicalTrades(self, symbol, limit=500, fromId=None):
        params = {"symbol": symbol, "limit": limit}
        if fromId:
            params['fromId'] = fromId
        ParameterValidator.validate_APIClient_params(**params)
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', 'historicalTrades', params=params)

    def get_klines(self, symbol, interval, startTime=None, endTime=None, timeZone="0", limit=500):
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "timeZone": timeZone
        }
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        ParameterValidator.validate_APIClient_params(**params)
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', 'klines', params=params)

    def get_ticker_24hr(self, symbol=None, symbols=None, dataType="FULL"):
        params = {
            "type": dataType
        }
        if symbol:
            params['symbol'] = symbol
        elif symbols:
            params['symbols'] = symbols
        ParameterValidator.validate_APIClient_params(**params)
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', 'ticker/24hr', params=params)

    def get_bookTicker(self, symbol=None, symbols=None):
        params = {}
        if symbol:
            params['symbol'] = symbol
        elif symbols:
            params['symbols'] = symbols
        ParameterValidator.validate_APIClient_params(**params)
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', 'ticker/bookTicker', params=params)

    def get_ticker_price(self, symbol=None, symbols=None):
        params = {}
        if symbol:
            params['symbol'] = symbol
        elif symbols:
            params['symbols'] = symbols
        ParameterValidator.validate_APIClient_params(**params)
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', 'ticker/price', params=params)

    def get_ticker_tradingDay(self, symbol=None, symbols=None, dataType="FULL", timeZone=0):
        params = {
            "type": dataType,
            "timeZone": timeZone
        }
        if symbol:
            params['symbol'] = symbol
        elif symbols:
            params['symbols'] = symbols
        ParameterValidator.validate_APIClient_params(**params)
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', 'ticker/tradingDay', params=params)

    def get_uiKlines(self, symbol, interval, startTime=None, endTime=None, timeZone="0", limit=500):
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": startTime,
            "endTime": endTime,
            "timeZone": timeZone,
            "limit": limit
        }
        ParameterValidator.validate_APIClient_params(**params)
        self._check_api_limits_before_request()
        return self.request_handler.retry_request('GET', 'uiKlines', params=params)
