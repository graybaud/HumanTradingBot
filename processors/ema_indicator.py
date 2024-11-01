from processors import Indicator

class EMAIndicator(Indicator):
    def compute(self, *args, **kwargs):
        close_prices = kwargs.get('close_prices')
        period = kwargs.get('period', 14)
        return close_prices.ewm(span=period, adjust=False).mean()