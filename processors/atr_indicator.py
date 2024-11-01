from processors import Indicator
from pandas import concat

class ATRIndicator(Indicator):
    def compute(self, *args, **kwargs):
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        close_prices = kwargs.get('close_prices')
        period = kwargs.get('period', 14)
        high_low = high_prices - low_prices
        high_close = (high_prices - close_prices.shift()).abs()
        low_close = (low_prices - close_prices.shift()).abs()
        true_range = concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        return atr