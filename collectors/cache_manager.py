import os
import json
import logging
import gzip

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, cache_dir="cache"):
        """
        :param cache_dir: Directory where cache files are stored.
        """
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _get_symbol_filepath(self, symbol):
        """
        :param symbol: Trading symbol (e.g., 'BTCUSDT').
        :return: Filepath for the symbol's JSON cache.
        """
        symbol_file = os.path.join(self.cache_dir, f"{symbol}_data.json.gz")
        return symbol_file

    def load_data(self, symbol):
        """
        :param symbol: Trading symbol.
        :return: Data as a dictionary or None if cache is empty/unavailable.
        """
        cache_file = self._get_symbol_filepath(symbol)
        if os.path.exists(cache_file):
            try:
                with gzip.open(cache_file, 'rt') as f:
                    logger.info(f"Loading cached data for {symbol}.")
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading cached data for {symbol}: {e}")
                return None
        else:
            logger.info(f"No cache found for {symbol}.")
            return None

    def store_data(self, symbol, data):
        """
        :param symbol: Trading symbol.
        :param data: Data to store (dictionary or DataFrame converted to dict).
        """
        cache_file = self._get_symbol_filepath(symbol)
        try:
            temp_file = f"{cache_file}.tmp"
            with gzip.open(temp_file, 'wt') as f:
                json.dump(data, f, indent=4, default=str)
            os.replace(temp_file, cache_file)
            logger.info(f"Data for {symbol} cached successfully.")
        except Exception as e:
            logger.error(f"Error caching data for {symbol}: {e}")

    def clear_cache(self):
        try:
            for root, _, files in os.walk(self.cache_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
            logger.info("Cache successfully cleared.")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")

    def store_exchange_info(self, exchange_info):
        """
        :param exchange_info: Exchange information.
        """
        cache_file = os.path.join(self.cache_dir, "exchange_info.json.gz")
        try:
            with gzip.open(cache_file, 'wt') as f:
                json.dump(exchange_info, f, indent=4)
                logger.info("Exchange information cached successfully.")
        except Exception as e:
            logger.error(f"Error caching exchange information: {e}")

    def load_exchange_info(self):
        """
        :return: Exchange information or None if cache is empty/unavailable.
        """
        cache_file = os.path.join(self.cache_dir, "exchange_info.json.gz")
        if os.path.exists(cache_file):
            try:
                with gzip.open(cache_file, 'rt') as f:
                    logger.info("Loading exchange information from cache.")
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading exchange information: {e}")
                return None
        else:
            logger.info("No cached exchange information found.")
            return None

    def store_account_info(self, account_info):
        """
        :param account_info: User account information.
        """
        cache_file = os.path.join(self.cache_dir, "account_info.json.gz")
        try:
            with gzip.open(cache_file, 'wt') as f:
                json.dump(account_info, f, indent=4)
                logger.info("Account information cached successfully.")
        except Exception as e:
            logger.error(f"Error caching account information: {e}")

    def load_account_info(self):
        """
        :return: Account information or None if cache is empty/unavailable.
        """
        cache_file = os.path.join(self.cache_dir, "account_info.json.gz")
        if os.path.exists(cache_file):
            try:
                with gzip.open(cache_file, 'rt') as f:
                    logger.info("Loading account information from cache.")
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading account information: {e}")
                return None
        else:
            logger.info("No cached account information found.")
            return None
