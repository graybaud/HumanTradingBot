import time
from Configuration import config

class RetryManager:
    def __init__(self):
        self.retries = config.RETRIES
        self.max_retry_time = config.MAX_RETRY_TIME

    def execute_with_retry(self, func, *args, **kwargs):
        start_time = time.time()
        for i in range(self.retries):
            if time.time() - start_time > self.max_retry_time:
                raise Exception("Max retry time exceeded.")
                # TODO : add logic to handle that case instead of raising exception
                # re-check if signals are stil relevant and/or order shoudl be executed or not after max_retry_time
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if i == self.retries - 1:
                    raise
                time.sleep(2 ** i)  # Exponential backoff
