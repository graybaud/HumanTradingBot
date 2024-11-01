from processors import Indicator

class SupportResistanceIndicator(Indicator):
    def compute(self, *args, **kwargs):
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        period = kwargs.get('period', 20)
        support = low_prices.rolling(window=period).min()
        resistance = high_prices.rolling(window=period).max()
        return support, resistance