from processors import Indicator, ATRIndicator

class KeltnerChannelsIndicator(Indicator):
    def compute(self, *args, **kwargs):
        close_prices = kwargs.get('close_prices')
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        period = kwargs.get('period', 20)
        atr_mult = kwargs.get('atr_mult', 2)
        ema = close_prices.ewm(span=period, adjust=False).mean()
        atr = ATRIndicator().compute(high_prices=high_prices, low_prices=low_prices, close_prices=close_prices, period=period)
        upper_band = ema + (atr_mult * atr)
        lower_band = ema - (atr_mult * atr)
        return upper_band, ema, lower_band
