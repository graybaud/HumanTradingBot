from HumanTradingBot.communication.request_handler import RequestHandler
from HumanTradingBot.communication.retry_manager import RetryManager
from HumanTradingBot.validator.parameter_validator import ParameterValidator
from Configuration import config
import time
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.request_handler = RequestHandler()  # Unique request handler for all subclasses
        self.retry_manager = RetryManager()  # Retry manager to handle limits and retries
        self.time_offset = self._get_time_offset()  # Time offset calculation

    def _get_time_offset(self):
        """
        Gets the time offset between the server and local machine.
        """
        response = self.request_handler.make_request('GET', 'time')
        server_time = response.json().get('serverTime')
        return int(time.time() * 1000) - server_time

    def _check_api_limits_before_request(self):
        """
        Checks the API rate limits before making a request and applies wait logic if needed.
        """
        if self.retry_manager.api_limits['request_weight'] >= config.MAX_REQUEST_WEIGHT:
            logger.warning("API request weight limit is close to being reached. Consider slowing down.")
            time.sleep(60)  # Sleep to avoid hitting rate limit => modify state_machine to force force sleep

        if self.retry_manager.api_limits['orders'] >= config.MAX_ORDER_COUNT:
            logger.warning("Order count limit is close to being reached.")
            # Additional logic to manage order count can be added here.
