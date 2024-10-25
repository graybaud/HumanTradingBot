import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self, api_client, cache_manager, error_manager, config_file):
        """
        Initializes the DataCollector.

        :param api_client: Instance to perform API calls
        :param cache_manager: Instance to manage data cache
        :param error_manager: Instance to handle errors
        :param config_file: Path to the configuration file
        """
        self.api_client = api_client
        self.cache_manager = cache_manager
        self.error_manager = error_manager
        self.config_file = config_file

        # Load symbols and timeframes from configuration
        self.symbols, self.timeframes = self.load_config()
        self.data = pd.DataFrame()
        self.initialized = False

    def load_config(self):
        """Loads symbols and timeframes from the configuration file."""
        # Example config format could be a JSON with {"symbols": [...], "timeframes": [...]}
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
            return config.get("symbols", []), config.get("timeframes", ["1h", "15m", "30m"])
        except Exception as e:
            self.error_manager.handle(e)
            return [], ["1h", "15m", "30m"]

    def initialize(self):
        """Initializes the collector by loading cached data and collecting any required exchange data."""
        if not self.initialized:
            self.load_cached_data()
            self.collect_exchange_info()
            self.initialized = True

    def load_cached_data(self):
        """Loads cached data or fetches new data if cache is empty."""
        for symbol in self.symbols:
            for timeframe in self.timeframes:
                try:
                    cached_data = self.cache_manager.load_data(symbol, timeframe)
                    if cached_data is not None:
                        self.data[(symbol, timeframe)] = cached_data
                    else:
                        self.collect_historical_data(symbol, timeframe)
                except Exception as e:
                    self.error_manager.handle(e)

    def collect_historical_data(self, symbol, timeframe):
        """
        Collects historical data for a given symbol and timeframe.

        :param symbol: The trading symbol (e.g., 'BTCUSDT')
        :param timeframe: The market data timeframe (e.g., '1h')
        """
        try:
            klines = self.api_client.get_historical_trades(symbol, timeframe)
            df = pd.DataFrame(klines, columns=[
                "open_time", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
            ])
            self.data[(symbol, timeframe)] = df
            self.cache_manager.store_data(symbol, timeframe, df)
        except Exception as e:
            self.error_manager.handle(e)

    def collect_periodic_data(self):
        """
        Collects periodic data for all symbols and timeframes.
        """
        for symbol in self.symbols:
            for timeframe in self.timeframes:
                try:
                    klines = self.api_client.get_klines(symbol, timeframe)
                    df = pd.DataFrame(klines, columns=[
                        "open_time", "open", "high", "low", "close", "volume",
                        "close_time", "quote_asset_volume", "number_of_trades",
                        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
                    ])
                    self.data[(symbol, timeframe)] = df
                    self.cache_manager.store_data(symbol, timeframe, df)
                except Exception as e:
                    self.error_manager.handle(e)

    def collect_exchange_info(self):
        """Retrieves and caches exchange information."""
        try:
            exchange_info = self.api_client.get_exchange_info()
            self.cache_manager.store_exchange_info(exchange_info)
        except Exception as e:
            self.error_manager.handle(e)

    def collect_account_info(self):
        """
        Retrieves user account information and stores it in `self.data`.
        """
        try:
            account_info = self.api_client.get_account_info()
            self.data['account_info'] = account_info
        except Exception as e:
            self.error_manager.handle(e)

    def refine_symbols(self, analysis_results, threshold):
        """
        Refines the list of symbols based on analysis results.

        :param analysis_results: Results from symbol analysis to determine the symbols/timeframes to monitor.
        """
        refined_symbols = [symbol for symbol, metrics in analysis_results.items() if metrics['score'] > threshold]
        self.symbols = refined_symbols  # Adjust symbols list based on analysis
        logger.info(f"Refined symbols list: {self.symbols}")
