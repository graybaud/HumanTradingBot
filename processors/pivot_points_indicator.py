from processors import Indicator

class PivotPointsIndicator(Indicator):
    def compute(self, *args, **kwargs):
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        close_prices = kwargs.get('close_prices')
        pivot = (high_prices + low_prices + close_prices) / 3
        resistance_1 = (2 * pivot) - low_prices
        support_1 = (2 * pivot) - high_prices
        return pivot, resistance_1, support_1