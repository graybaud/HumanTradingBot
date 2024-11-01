from processors import Indicator

class RSIIndicator(Indicator):
    def compute(self, *args, **kwargs):
        close_prices = kwargs.get('close_prices')
        period = kwargs.get('period', 14)
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi