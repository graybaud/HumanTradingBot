from processors import Indicator

class BollingerBandsIndicator(Indicator):
    def compute(self, *args, **kwargs):
        close_prices = kwargs.get('close_prices')
        period = kwargs.get('period', 20)
        std_dev = kwargs.get('std_dev', 2)
        sma = close_prices.rolling(window=period).mean()
        rolling_std = close_prices.rolling(window=period).std()
        upper_band = sma + (rolling_std * std_dev)
        lower_band = sma - (rolling_std * std_dev)
        return upper_band, sma, lower_band