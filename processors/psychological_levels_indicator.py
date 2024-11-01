from processors import Indicator

class PsychologicalLevelsIndicator(Indicator):
    def compute(self, *args, **kwargs):
        close_prices = kwargs.get('close_prices')
        return close_prices.apply(lambda x: round(x, -len(str(int(x))) + 1))