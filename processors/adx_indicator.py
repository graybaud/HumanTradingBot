from processors import Indicator, ATRIndicator
from pandas import Series
import numpy as np

class ADXIndicator(Indicator):
    def compute(self, *args, **kwargs):
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        close_prices = kwargs.get('close_prices')
        period = kwargs.get('period', 14)
        up_move = high_prices.diff()
        down_move = low_prices.diff()
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        atr = ATRIndicator().compute(high_prices=high_prices, low_prices=low_prices, close_prices=close_prices, period=period)
        plus_di = 100 * (Series(plus_dm).rolling(window=period).mean() / atr)
        minus_di = 100 * (Series(minus_dm).rolling(window=period).mean() / atr)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        adx = dx.rolling(window=period).mean()
        return adx