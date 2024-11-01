from processors import Indicator

class StochasticIndicator(Indicator):
    def compute(self, *args, **kwargs):
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        close_prices = kwargs.get('close_prices')
        k_period = kwargs.get('k_period', 14)
        d_period = kwargs.get('d_period', 3)
        low_k = low_prices.rolling(window=k_period).min()
        high_k = high_prices.rolling(window=k_period).max()
        k_value = 100 * (close_prices - low_k) / (high_k - low_k)
        d_value = k_value.rolling(window=d_period).mean()
        return k_value, d_value