from HumanTradingBot.communication.api_client import APIClient
from HumanTradingBot.validator.parameter_validator import ParameterValidator

class UserData(APIClient):
    def __init__(self):
        super().__init__()  # Inherits request_handler, retry_manager, and time_offset
