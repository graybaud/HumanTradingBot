from processors import Indicator


class IchimokuCloudIndicator(Indicator):
    def compute(self, *args, **kwargs):
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        close_prices = kwargs.get('close_prices')
        period_tenkan = kwargs.get('period_tenkan', 9)
        period_kijun = kwargs.get('period_kijun', 26)
        period_senkou = kwargs.get('period_senkou', 52)
        tenkan_sen = (high_prices.rolling(window=period_tenkan).max() + low_prices.rolling(window=period_tenkan).min()) / 2
        kijun_sen = (high_prices.rolling(window=period_kijun).max() + low_prices.rolling(window=period_kijun).min()) / 2
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(period_kijun)
        senkou_span_b = ((high_prices.rolling(window=period_senkou).max() + low_prices.rolling(window=period_senkou).min()) / 2).shift(period_kijun)
        chikou_span = close_prices.shift(-period_kijun)
        return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span
