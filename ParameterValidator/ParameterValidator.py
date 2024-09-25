class ParameterValidator:

    @staticmethod
    def validate_positive_number(value, param_name):
        """Valide que la valeur est un nombre positif."""
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"Invalid {param_name}: {value} ,must be a positive number")

    @staticmethod
    def validate_order_list_id(value, param_name):
        """Valide que l'order_list_id est un entier positif ou égal à -1."""
        if not isinstance(value, (int, float)) or (value != -1 and value <= 0):
            raise ValueError(f"Invalid {param_name}: {value} ,must be a positive integer or -1")

    @staticmethod
    def validate_string(value, param_name):
        """Valide que le valeur est une chaîne non vide."""
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError(f"Invalid {param_name}: {value} ,must be a non-empty string")

    @staticmethod
    def validate_in_options(value, valid_options, param_name):
        """Valide que la valeur fait partie des options valides."""
        if value not in valid_options:
            raise ValueError(f"Invalid {param_name}: {value} ,must be one of {valid_options}")

    @staticmethod
    def validate_side(side):
        """Valide que le côté est soit 'BUY' soit 'SELL'."""
        ParameterValidator.validate_in_options(side, ["BUY", "SELL"], "side")

    @staticmethod
    def validate_orderType(order_type):
        """Valide que le type de commande est valide."""
        ParameterValidator.validate_in_options(
            order_type,
            ["LIMIT", "MARKET", "STOP_LOSS", "STOP_LOSS_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT", "LIMIT_MAKER"],
            "order type"
            )

    @staticmethod
    def validate_symbol(symbol):
        """Valide que le symbole est une chaîne non vide."""
        ParameterValidator.validate_string(symbol, "symbol")

    @staticmethod
    def validate_quantity(quantity):
        """Valide que la quantité est un nombre positif."""
        ParameterValidator.validate_positive_number(quantity, "quantity")

    @staticmethod
    def validate_price(price):
        """Valide que le prix est un nombre positif."""
        ParameterValidator.validate_positive_number(price, "price")

    @staticmethod
    def validate_stopPrice(stopPrice):
        """Valide que le stopPrice est un nombre positif."""
        ParameterValidator.validate_positive_number(stopPrice, "stop price")

    @staticmethod
    def validate_stopLimitPrice(stopLimitPrice):
        """Valide que le stopLimitPrice est un nombre positif."""
        ParameterValidator.validate_positive_number(stopLimitPrice, "stop limit price")

    @staticmethod
    def validate_orderId(orderId):
        """Valide que l'identifiant de l'ordre est un entier positif."""
        ParameterValidator.validate_positive_number(orderId, "order id")

    @staticmethod
    def validate_listenKey(listenKey):
        """Valide que la clé d'écoute est une chaîne non vide."""
        ParameterValidator.validate_string(listenKey, "listen key")

    @staticmethod
    def validate_timestamp(timestamp):
        """Valide que le timestamp est un entier positif."""
        ParameterValidator.validate_positive_number(timestamp, "timestamp")

    @staticmethod
    def validate_timeInForce(timeInForce):
        """Valide que le timeInForce est une des valeurs valides."""
        ParameterValidator.validate_in_options(timeInForce, ["GTC", "IOC", "FOK"], "timeInForce")

    @staticmethod
    def validate_recvWindow(recvWindow):
        """Valide que recvWindow est un entier positif."""
        ParameterValidator.validate_positive_number(recvWindow, "recv window")

    @staticmethod
    def validate_limit(limit):
        """Valide que le limit est un entier positif."""
        ParameterValidator.validate_positive_number(limit, "limit")

    @staticmethod
    def validate_APIClient_params(**params):
        """Valide les paramètres en fonction de ceux fournis."""

        validation_mapping = {
            'symbol': ParameterValidator.validate_symbol,
            'side': ParameterValidator.validate_side,
            'quantity': ParameterValidator.validate_quantity,
            'price': ParameterValidator.validate_price,
            'stopPrice': ParameterValidator.validate_stopPrice,
            'stopLimitPrice': ParameterValidator.validate_stopLimitPrice,
            'orderId': ParameterValidator.validate_orderId,
            'listenKey': ParameterValidator.validate_listenKey,
            'orderType': ParameterValidator.validate_orderType,
            'limit': ParameterValidator.validate_limit,
            'timestamp': ParameterValidator.validate_timestamp,
            'recvWindow': ParameterValidator.validate_recvWindow,
            'timeInForce': ParameterValidator.validate_timeInForce
        }

        for param_name, param_value in params.items():
            if param_value is not None and param_name in validation_mapping:
                validation_mapping[param_name](param_value)
