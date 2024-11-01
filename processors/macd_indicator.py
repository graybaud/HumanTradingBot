from processors import Indicator

class MACDIndicator(Indicator):
    def compute(self, *args, **kwargs):
        close_prices = kwargs.get('close_prices')
        short_period = kwargs.get('short_period', 12)
        long_period = kwargs.get('long_period', 26)
        signal_period = kwargs.get('signal_period', 9)
        short_ema = close_prices.ewm(span=short_period, adjust=False).mean()
        long_ema = close_prices.ewm(span=long_period, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        return macd_line, signal_line