import unittest
from ParameterValidator.ParameterValidator import ParameterValidator

class TestParameterValidator(unittest.TestCase):
    
    def test_validate_positive_number(self):
        # Cas valide
        ParameterValidator.validate_positive_number(10, "test_param")
        
        # Cas d'erreur : valeur négative
        with self.assertRaises(ValueError):
            ParameterValidator.validate_positive_number(-5, "test_param")
        
        # Cas d'erreur : valeur zéro
        with self.assertRaises(ValueError):
            ParameterValidator.validate_positive_number(0, "test_param")
        
        # Cas d'erreur : type incorrect
        with self.assertRaises(ValueError):
            ParameterValidator.validate_positive_number("invalid", "test_param")

    def test_validate_order_list_id(self):
        # Cas valide : positif
        ParameterValidator.validate_order_list_id(1, "order_list_id")
        
        # Cas valide : -1
        ParameterValidator.validate_order_list_id(-1, "order_list_id")
        
        # Cas d'erreur : nombre négatif autre que -1
        with self.assertRaises(ValueError):
            ParameterValidator.validate_order_list_id(-5, "order_list_id")
        
        # Cas d'erreur : type incorrect
        with self.assertRaises(ValueError):
            ParameterValidator.validate_order_list_id("invalid", "order_list_id")

    def test_validate_string(self):
        # Cas valide
        ParameterValidator.validate_string("valid_string", "test_param")
        
        # Cas d'erreur : chaîne vide
        with self.assertRaises(ValueError):
            ParameterValidator.validate_string("", "test_param")
        
        # Cas d'erreur : type incorrect
        with self.assertRaises(ValueError):
            ParameterValidator.validate_string(123, "test_param")

    def test_validate_in_options(self):
        # Cas valide
        ParameterValidator.validate_in_options("BUY", ["BUY", "SELL"], "side")
        
        # Cas d'erreur : option invalide
        with self.assertRaises(ValueError):
            ParameterValidator.validate_in_options("INVALID", ["BUY", "SELL"], "side")

    def test_validate_side(self):
        # Cas valide
        ParameterValidator.validate_side("BUY")
        
        # Cas d'erreur
        with self.assertRaises(ValueError):
            ParameterValidator.validate_side("INVALID")

    def test_validate_orderType(self):
        # Cas valide
        ParameterValidator.validate_orderType("LIMIT")
        
        # Cas d'erreur
        with self.assertRaises(ValueError):
            ParameterValidator.validate_orderType("INVALID")

    def test_validate_symbol(self):
        # Cas valide
        ParameterValidator.validate_symbol("BTCUSD")
        
        # Cas d'erreur : chaîne vide
        with self.assertRaises(ValueError):
            ParameterValidator.validate_symbol("")

    def test_validate_quantity(self):
        # Cas valide
        ParameterValidator.validate_quantity(10)
        
        # Cas d'erreur : valeur négative
        with self.assertRaises(ValueError):
            ParameterValidator.validate_quantity(-10)

    def test_validate_price(self):
        # Cas valide
        ParameterValidator.validate_price(100.50)
        
        # Cas d'erreur : zéro ou négatif
        with self.assertRaises(ValueError):
            ParameterValidator.validate_price(0)

    def test_validate_stopPrice(self):
        # Cas valide
        ParameterValidator.validate_stopPrice(50)
        
        # Cas d'erreur : négatif
        with self.assertRaises(ValueError):
            ParameterValidator.validate_stopPrice(-50)

    def test_validate_stopLimitPrice(self):
        # Cas valide
        ParameterValidator.validate_stopLimitPrice(50)
        
        # Cas d'erreur : négatif
        with self.assertRaises(ValueError):
            ParameterValidator.validate_stopLimitPrice(-50)

    def test_validate_orderId(self):
        # Cas valide
        ParameterValidator.validate_orderId(12345)
        
        # Cas d'erreur : négatif
        with self.assertRaises(ValueError):
            ParameterValidator.validate_orderId(-1)

    def test_validate_listenKey(self):
        # Cas valide
        ParameterValidator.validate_listenKey("valid_key")
        
        # Cas d'erreur : chaîne vide
        with self.assertRaises(ValueError):
            ParameterValidator.validate_listenKey("")

    def test_validate_timestamp(self):
        # Cas valide
        ParameterValidator.validate_timestamp(1633046400)
        
        # Cas d'erreur : négatif
        with self.assertRaises(ValueError):
            ParameterValidator.validate_timestamp(-1)

    def test_validate_timeInForce(self):
        # Cas valide
        ParameterValidator.validate_timeInForce("GTC")
        
        # Cas d'erreur : option invalide
        with self.assertRaises(ValueError):
            ParameterValidator.validate_timeInForce("INVALID")

    def test_validate_recvWindow(self):
        # Cas valide
        ParameterValidator.validate_recvWindow(5000)
        
        # Cas d'erreur : négatif
        with self.assertRaises(ValueError):
            ParameterValidator.validate_recvWindow(-1)

    def test_validate_limit(self):
        # Cas valide
        ParameterValidator.validate_limit(10)
        
        # Cas d'erreur : négatif
        with self.assertRaises(ValueError):
            ParameterValidator.validate_limit(-10)

    def test_validate_APIClient_params(self):
        # Test avec plusieurs paramètres valides
        params = {
            'symbol': "BTCUSD",
            'side': "BUY",
            'quantity': 10,
            'price': 50000,
            'stopPrice': 49000,
            'orderType': "LIMIT",
            'timestamp': 1633046400
        }
        ParameterValidator.validate_APIClient_params(**params)
        
        # Cas d'erreur avec un paramètre invalide
        params['price'] = -50000  # Prix négatif
        with self.assertRaises(ValueError):
            ParameterValidator.validate_APIClient_params(**params)

if __name__ == '__main__':
    unittest.main()
