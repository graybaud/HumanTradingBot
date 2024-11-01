from processors import Indicator
from pandas import cut

class VolumeProfileIndicator(Indicator):
    def compute(self, *args, **kwargs):
        close_prices = kwargs.get('close_prices')
        bins = kwargs.get('bins', 10)
        volume_profile = cut(close_prices, bins=bins).value_counts()
        return volume_profile