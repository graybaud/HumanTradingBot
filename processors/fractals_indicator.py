from processors import Indicator

class FractalsIndicator(Indicator):
    def compute(self, *args, **kwargs):
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        period = kwargs.get('period', 5)
        high_fractal = (high_prices == high_prices.rolling(window=period, center=True).max())
        low_fractal = (low_prices == low_prices.rolling(window=period, center=True).min())
        return high_fractal, low_fractal