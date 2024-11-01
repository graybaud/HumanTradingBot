from processors import Indicator

class CCIIndicator(Indicator):
    def compute(self, *args, **kwargs):
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        close_prices = kwargs.get('close_prices')
        period = kwargs.get('period', 20)
        typical_price = (high_prices + low_prices + close_prices) / 3
        sma = typical_price.rolling(window=period).mean()
        mean_deviation = (typical_price - sma).abs().rolling(window=period).mean()
        cci = (typical_price - sma) / (0.015 * mean_deviation)
        return cci