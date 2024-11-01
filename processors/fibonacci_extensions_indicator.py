from processors import Indicator

class FibonacciExtensionsIndicator(Indicator):
    def compute(self, *args, **kwargs):
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        levels = kwargs.get('levels', [0.236, 0.382, 0.618, 0.5, 0.786, 1.0])
        price_diff = high_prices.max() - low_prices.min()
        extensions = {level: high_prices.max() + price_diff * level for level in levels}
        return extensions