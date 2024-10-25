from HumanTradingBot.communication.api_client import APIClient
from HumanTradingBot.validator.parameter_validator import ParameterValidator

class TradeEndpoints(APIClient):
    def __init__(self, request_handler, retry_manager, time_offset):
        super().__init__(request_handler, retry_manager, time_offset)
    
    def _prepare_and_validate_params(self, params):
        ParameterValidator.validate_APIClient_params(**params)
        self._check_api_limits_before_request()
        return self.request_handler._add_security_params(params)

    def order_DELETE(self, params):
        params = self._prepare_and_validate_params(params)
        return self.request_handler.retry_request('DELETE', 'order', params=params)

    def order_GET(self, symbol, orderId=None, origClientOrderId=None):
        params = {
            'symbol': symbol,
        }
        if orderId:
            params['orderId'] = orderId
        if origClientOrderId:
            params['origClientOrderId'] = origClientOrderId

        params = self._prepare_and_validate_params(params)
        return self.request_handler.retry_request('GET', 'order', params=params)

    def order_test_POST(self, symbol, side, type, timeInForce=None, quantity=None, price=None, computeCommissionRates=False, **kwargs):
        params = {k: v for k, v in {
            'symbol': symbol,
            'side': side,
            'type': type,
            'timeInForce': timeInForce,
            'quantity': quantity,
            'price': price,
            'computeCommissionRates': computeCommissionRates
        }.items() if v is not None}

        params.update(kwargs)
        params = self._prepare_and_validate_params(params)
        return self.request_handler.retry_request('POST', 'order_test', params=params)

    def order_POST(self, params: dict):

        # TODO : to be move into order preparation
        # Check if quantity or quoteOrderQty is provided based on the order type
        if params.get('type') == 'MARKET' and not ('quantity' in params or 'quoteOrderQty' in params):
            raise ValueError("For MARKET orders, either 'quantity' or 'quoteOrderQty' must be provided.")

        # Ensure price and timeInForce are present for LIMIT orders
        if params.get('type') == 'LIMIT' and not ('price' in params and 'timeInForce' in params):
            raise ValueError("For LIMIT orders, 'price' and 'timeInForce' are required.")

        # Ensure stopPrice or trailingDelta is present for stop orders
        stop_order_types = ['STOP_LOSS', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT']
        if params.get('type') in stop_order_types and not ('stopPrice' in params or 'trailingDelta' in params):
            raise ValueError(f"For {params.get('type')} orders, either 'stopPrice' or 'trailingDelta' must be provided.")
        
        params = self._prepare_and_validate_params(params)
        return self.request_handler.retry_request("POST","order",params)

    def cancelReplace_POST(self, symbol, side, order_type, cancelOrderId, cancel_replace_mode, new_order_params):
        ParameterValidator.validate_APIClient_params(**new_order_params)
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "cancelReplaceMode": cancel_replace_mode,
            "cancelOrderId": cancelOrderId,
        }

        if new_order_params:
            params.update(new_order_params)
        params = self._prepare_and_validate_params(params)
        return self.request_handler.retry_request("POST", "cancel_replace_order", params)

    def order_list_oco_POST(self, symbol, side, quantity, above_type, below_type, timestamp, 
                            above_client_order_id=None, above_iceberg_qty=None, above_price=None, 
                            above_stop_price=None, above_trailing_delta=None, above_time_in_force=None, 
                            above_strategy_id=None, above_strategy_type=None,below_client_order_id=None,
                            below_iceberg_qty=None, below_price=None, below_stop_price=None,
                            below_trailing_delta=None, below_time_in_force=None, below_strategy_id=None,
                            below_strategy_type=None, list_client_order_id=None, new_order_resp_type=None, 
                            self_trade_prevention_mode=None, recv_window=None):
        
        endpoint = '/api/v3/orderList/oco'
        params = {
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'aboveType': above_type,
            'belowType': below_type,
            'timestamp': timestamp
        }
        
        if above_client_order_id:
            params['aboveClientOrderId'] = above_client_order_id
        if above_iceberg_qty:
            params['aboveIcebergQty'] = above_iceberg_qty
        if above_price:
            params['abovePrice'] = above_price
        if above_stop_price:
            params['aboveStopPrice'] = above_stop_price
        if above_trailing_delta:
            params['aboveTrailingDelta'] = above_trailing_delta
        if above_time_in_force:
            params['aboveTimeInForce'] = above_time_in_force
        if above_strategy_id:
            params['aboveStrategyId'] = above_strategy_id
        if above_strategy_type:
            params['aboveStrategyType'] = above_strategy_type
        
        if below_client_order_id:
            params['belowClientOrderId'] = below_client_order_id
        if below_iceberg_qty:
            params['belowIcebergQty'] = below_iceberg_qty
        if below_price:
            params['belowPrice'] = below_price
        if below_stop_price:
            params['belowStopPrice'] = below_stop_price
        if below_trailing_delta:
            params['belowTrailingDelta'] = below_trailing_delta
        if below_time_in_force:
            params['belowTimeInForce'] = below_time_in_force
        if below_strategy_id:
            params['belowStrategyId'] = below_strategy_id
        if below_strategy_type:
            params['belowStrategyType'] = below_strategy_type
        
        if list_client_order_id:
            params['listClientOrderId'] = list_client_order_id
        if new_order_resp_type:
            params['newOrderRespType'] = new_order_resp_type
        if self_trade_prevention_mode:
            params['selfTradePreventionMode'] = self_trade_prevention_mode
        if recv_window:
            params['recvWindow'] = recv_window
        params = self._prepare_and_validate_params(params)
        return self.request_handler.retry_request('POST', endpoint, params=params)

    def order_OCO_POST(self, symbol, side, quantity, price, stopPrice, listClientOrderId=None,
                       limitClientOrderId=None, limitStrategyId=None,limitStrategyType=None,
                       limitIcebergQty=None, trailingDelta=None, stopClientOrderId=None,
                       stopStrategyId=None, stopStrategyType=None, stopLimitPrice=None,
                       stopIcebergQty=None, stopLimitTimeInForce=None, newOrderRespType=None,
                       selfTradePreventionMode=None, recvWindow=None, **kwargs):
        
        params = {
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': price,
            'stopPrice': stopPrice,
        }

        # Adding optional parameters if provided
        if listClientOrderId:
            params['listClientOrderId'] = listClientOrderId
        if limitClientOrderId:
            params['limitClientOrderId'] = limitClientOrderId
        if limitStrategyId:
            params['limitStrategyId'] = limitStrategyId
        if limitStrategyType:
            params['limitStrategyType'] = limitStrategyType
        if limitIcebergQty:
            params['limitIcebergQty'] = limitIcebergQty
        if trailingDelta:
            params['trailingDelta'] = trailingDelta
        if stopClientOrderId:
            params['stopClientOrderId'] = stopClientOrderId
        if stopStrategyId:
            params['stopStrategyId'] = stopStrategyId
        if stopStrategyType:
            params['stopStrategyType'] = stopStrategyType
        if stopLimitPrice:
            params['stopLimitPrice'] = stopLimitPrice
        if stopIcebergQty:
            params['stopIcebergQty'] = stopIcebergQty
        if stopLimitTimeInForce:
            params['stopLimitTimeInForce'] = stopLimitTimeInForce
        if newOrderRespType:
            params['newOrderRespType'] = newOrderRespType
        if selfTradePreventionMode:
            params['selfTradePreventionMode'] = selfTradePreventionMode
        if recvWindow:
            params['recvWindow'] = recvWindow
        
        # Adding additional keyword arguments
        params.update(kwargs)
        
        # Validate the parameters
        ParameterValidator.validate_APIClient_params(**params)
        
        # Check API limits and add security params
        self._check_api_limits_before_request()
        params = self.request_handler._add_security_params(params)
        
        # Send request
        response = self.request_handler.retry_request('POST', 'order/oco', params=params)
        
        return response


    def orderList_oto_POST(self, symbol, workingType, workingSide, workingPrice, workingQuantity, pendingType, pendingSide, pendingQuantity, **kwargs):
        params = {
            'symbol': symbol,
            'workingType': workingType,
            'workingSide': workingSide,
            'workingPrice': workingPrice,
            'workingQuantity': workingQuantity,
            'pendingType': pendingType,
            'pendingSide': pendingSide,
            'pendingQuantity': pendingQuantity,
            'timestamp': self._get_server_time(),
        }
        params.update(kwargs)

        ParameterValidator.validate_APIClient_params(**params)

        # Validation for LIMIT orders
        if workingType == 'LIMIT' and 'workingTimeInForce' not in params:
            raise ValueError("For LIMIT working orders, 'workingTimeInForce' is required.")
        
        if pendingType == 'LIMIT' and ('pendingPrice' not in params or 'pendingTimeInForce' not in params):
            raise ValueError("For LIMIT pending orders, 'pendingPrice' and 'pendingTimeInForce' are required.")
        
        # Validation for STOP_LOSS or TAKE_PROFIT
        if pendingType in ['STOP_LOSS', 'TAKE_PROFIT'] and not ('pendingStopPrice' in params or 'pendingTrailingDelta' in params):
            raise ValueError(f"For {pendingType} orders, either 'pendingStopPrice' or 'pendingTrailingDelta' must be provided.")
        
        # Validation for STOP_LOSS_LIMIT or TAKE_PROFIT_LIMIT
        if pendingType in ['STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'] and (not ('pendingPrice' in params and 'pendingStopPrice' in params) and 'pendingTimeInForce' not in params):
            raise ValueError(f"For {pendingType} orders, 'pendingPrice', 'pendingStopPrice' and 'pendingTimeInForce' are required.")

        self._check_api_limits_before_request()
        params = self.request_handler._add_security_params(params)

        response = self.request_handler.retry_request('POST', 'orderList/oto', params=params)

        return response
    
    def place_otoco_order(self, symbol: str, workingType: str, workingSide: str, workingPrice: float, 
                          workingQuantity: float, pendingSide: str, pendingQuantity: float, 
                          pendingAboveType: str, pendingBelowType: str, 
                          timestamp: int, listClientOrderId: Optional[str] = None, 
                          newOrderRespType: Optional[str] = None, selfTradePreventionMode: Optional[str] = None, 
                          workingClientOrderId: Optional[str] = None, workingIcebergQty: Optional[float] = None, 
                          workingTimeInForce: Optional[str] = None, workingStrategyId: Optional[int] = None, 
                          workingStrategyType: Optional[int] = None, pendingAboveClientOrderId: Optional[str] = None, 
                          pendingAbovePrice: Optional[float] = None, pendingAboveStopPrice: Optional[float] = None, 
                          pendingAboveTrailingDelta: Optional[float] = None, pendingAboveIcebergQty: Optional[float] = None, 
                          pendingAboveTimeInForce: Optional[str] = None, pendingAboveStrategyId: Optional[int] = None, 
                          pendingAboveStrategyType: Optional[int] = None, pendingBelowClientOrderId: Optional[str] = None, 
                          pendingBelowPrice: Optional[float] = None, pendingBelowStopPrice: Optional[float] = None, 
                          pendingBelowTrailingDelta: Optional[float] = None, pendingBelowIcebergQty: Optional[float] = None, 
                          pendingBelowTimeInForce: Optional[str] = None, pendingBelowStrategyId: Optional[int] = None, 
                          pendingBelowStrategyType: Optional[int] = None, recvWindow: Optional[int] = 5000):
        """
        Place an OTOCO order (One-Triggers-One-Cancels-the-Other) that includes a working order and 
        two pending orders (OCO pair).

        :param symbol: Trading symbol (e.g., BTCUSDT).
        :param workingType: Type of the working order (LIMIT, LIMIT_MAKER).
        :param workingSide: Side of the working order (BUY or SELL).
        :param workingPrice: Price for the working order.
        :param workingQuantity: Quantity for the working order.
        :param pendingSide: Side of the pending orders (BUY or SELL).
        :param pendingQuantity: Quantity for the pending orders.
        :param pendingAboveType: Type of the pending above order (LIMIT_MAKER, STOP_LOSS, STOP_LOSS_LIMIT).
        :param pendingBelowType: Type of the pending below order (LIMIT_MAKER, STOP_LOSS, STOP_LOSS_LIMIT).
        :param timestamp: Request timestamp in milliseconds.
        :param listClientOrderId: Optional ID to uniquely identify the order list.
        :param newOrderRespType: Optional response type (ACK, RESULT, FULL).
        :param recvWindow: The value cannot be greater than 60000.
        :param Other Optional Parameters: Additional parameters based on the pendingAboveType, pendingBelowType or workingType.
        :return: JSON response with order details.
        """
        params = {
            'symbol': symbol,
            'workingType': workingType,
            'workingSide': workingSide,
            'workingPrice': workingPrice,
            'workingQuantity': workingQuantity,
            'pendingSide': pendingSide,
            'pendingQuantity': pendingQuantity,
            'pendingAboveType': pendingAboveType,
            'pendingBelowType': pendingBelowType,
            'timestamp': timestamp
        }

        # Optional parameters
        if listClientOrderId:
            params['listClientOrderId'] = listClientOrderId
        if newOrderRespType:
            params['newOrderRespType'] = newOrderRespType
        if selfTradePreventionMode:
            params['selfTradePreventionMode'] = selfTradePreventionMode
        if workingClientOrderId:
            params['workingClientOrderId'] = workingClientOrderId
        if workingIcebergQty:
            params['workingIcebergQty'] = workingIcebergQty
        if workingTimeInForce:
            params['workingTimeInForce'] = workingTimeInForce
        if workingStrategyId:
            params['workingStrategyId'] = workingStrategyId
        if workingStrategyType:
            params['workingStrategyType'] = workingStrategyType
        if pendingAboveClientOrderId:
            params['pendingAboveClientOrderId'] = pendingAboveClientOrderId
        if pendingAbovePrice:
            params['pendingAbovePrice'] = pendingAbovePrice
        if pendingAboveStopPrice:
            params['pendingAboveStopPrice'] = pendingAboveStopPrice
        if pendingAboveTrailingDelta:
            params['pendingAboveTrailingDelta'] = pendingAboveTrailingDelta
        if pendingAboveIcebergQty:
            params['pendingAboveIcebergQty'] = pendingAboveIcebergQty
        if pendingAboveTimeInForce:
            params['pendingAboveTimeInForce'] = pendingAboveTimeInForce
        if pendingAboveStrategyId:
            params['pendingAboveStrategyId'] = pendingAboveStrategyId
        if pendingAboveStrategyType:
            params['pendingAboveStrategyType'] = pendingAboveStrategyType
        if pendingBelowClientOrderId:
            params['pendingBelowClientOrderId'] = pendingBelowClientOrderId
        if pendingBelowPrice:
            params['pendingBelowPrice'] = pendingBelowPrice
        if pendingBelowStopPrice:
            params['pendingBelowStopPrice'] = pendingBelowStopPrice
        if pendingBelowTrailingDelta:
            params['pendingBelowTrailingDelta'] = pendingBelowTrailingDelta
        if pendingBelowIcebergQty:
            params['pendingBelowIcebergQty'] = pendingBelowIcebergQty
        if pendingBelowTimeInForce:
            params['pendingBelowTimeInForce'] = pendingBelowTimeInForce
        if pendingBelowStrategyId:
            params['pendingBelowStrategyId'] = pendingBelowStrategyId
        if pendingBelowStrategyType:
            params['pendingBelowStrategyType'] = pendingBelowStrategyType
        if recvWindow:
            params['recvWindow'] = recvWindow

        return self.request_handler.retry_request('POST', '/api/v3/orderList/otoco', params=params)