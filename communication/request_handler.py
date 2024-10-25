import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from Configuration import config
from HumanTradingBot.communication.retry_manager import RetryManager
from HumanTradingBot.communication.response_handler import ResponseHandler

class RequestHandler:
    def __init__(self):
        self.api_key = config.API_KEY
        self.api_secret = config.SECRET_KEY
        self.base_url = config.BASE_URLS[0]
        # TODO optionnal : add logic to go through all base_url,
        # in case of one base_url failed after multiple atempt
        
        self.retry_manager =  RetryManager()
        self.response_handler =  ResponseHandler()

    def _get_headers(self):
        return {"X-MBX-APIKEY": self.api_key}

    def _add_security_params(self, params):
        """Ajoute les paramètres de sécurité pour les requêtes SIGNED."""
        params['timestamp'] = int(time.time() * 1000 + self.time_offset)
        params['recvWindow'] = self.recvWindow
        return params

    def _sign(self, params):
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

    def retry_request(self, method, endpoint, params=None, data=None, weight=1):
        if params is None:
            params = {}

        endpointUrl = config.ENDPOINTS.get(endpoint)
        if not endpointUrl:
            raise ValueError(f"Endpoint '{endpointUrl}' not found in configuration.")

        url = f"{self.base_url}{endpointUrl}"
        headers = self._get_headers()

        if not self.retry_manager.can_make_request(weight):
            time.sleep(60)  # Attend avant de refaire une requête
            return self.retry_request(method, endpoint, params, data, weight)

        return self.retry_manager.execute_with_retry(
            self._send_http_request, method, url, headers, params, data
        )

    def _send_http_request(self, method, url, headers, params=None, data=None):
        response = requests.request(method, url, headers=headers, params=params, data=data)
        return self.response_handler.handle(response)
