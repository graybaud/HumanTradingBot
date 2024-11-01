from processors import Indicator

class IndicatorManager:
    def __init__(self):
        self.indicators = []

    def add_indicator(self, indicator):
        if isinstance(indicator, Indicator):
            self.indicators.append(indicator)
        else:
            raise TypeError("Only instances of Indicator can be added")

    def compute_all(self, *args, **kwargs):
        results = {}
        for indicator in self.indicators:
            result = indicator.compute(*args, **kwargs)
            results[indicator.__class__.__name__] = result
        return results
