from processors import Indicator

class VWAPIndicator(Indicator):
    def compute(self, *args, **kwargs):
        close_prices = kwargs.get('close_prices')
        volumes = kwargs.get('volumes')
        return (volumes * close_prices).cumsum() / volumes.cumsum()