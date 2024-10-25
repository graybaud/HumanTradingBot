import time
from Configuration import config
import logging

logger = logging.getLogger(__name__)

class RetryManager:
    def __init__(self):
        self.retries = config.RETRIES
        self.max_retry_time = config.MAX_RETRY_TIME
        self.api_limits = {
            "request_weight": 0,
            "orders": 0,
        }

    def _check_api_limits(self, headers):
        """Mise à jour des limites API à partir des headers."""
        self.api_limits['request_weight'] = int(headers.get('X-MBX-USED-WEIGHT-1M', 0))
        self.api_limits['orders'] = int(headers.get('X-MBX-USED-ORDER-COUNT-1M', 0))
        logger.info(f"Current API Limits - Request Weight: {self.api_limits['request_weight']}, Orders: {self.api_limits['orders']}")

    def can_make_request(self, request_weight):
        """Vérifie si l'appel API peut être effectué selon les limites actuelles."""
        if self.api_limits['request_weight'] + request_weight > self.weight_threshold:
            logger.warning("API weight limit is close to being exceeded.")
            return False
        return True

    def execute_with_retry(self, func, *args, **kwargs):
        start_time = time.time()
        for i in range(self.retries):
            if time.time() - start_time > self.max_retry_time:
                raise Exception("Max retry time exceeded.")
            try:
                response = func(*args, **kwargs)
                self._check_api_limits(response.headers)  # Check headers for API limits
                return response
            except Exception as e:
                if i == self.retries - 1:
                    raise
                time.sleep(2 ** i)  # Exponential backoff
