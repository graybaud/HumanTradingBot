from processors import Indicator
from pandas import Series

class ParabolicSARIndicator(Indicator):
    def compute(self, *args, **kwargs):
        high_prices = kwargs.get('high_prices')
        low_prices = kwargs.get('low_prices')
        close_prices = kwargs.get('close_prices')
        step = kwargs.get('step', 0.02)
        max_step = kwargs.get('max_step', 0.2)
        sar = [close_prices[0]]
        ep = high_prices[0]
        acceleration_factor = step
        trend = True

        for i in range(1, len(close_prices)):
            new_sar = sar[i - 1] + acceleration_factor * (ep - sar[i - 1])
            ep = max(ep, high_prices[i]) if trend else min(ep, low_prices[i])

            if trend:
                new_sar = min(new_sar, low_prices[i], low_prices[i - 1])
                if low_prices[i] < new_sar:
                    trend = False
                    acceleration_factor = step
                    ep = low_prices[i]
            else:
                new_sar = max(new_sar, high_prices[i], high_prices[i - 1])
                if high_prices[i] > new_sar:
                    trend = True
                    acceleration_factor = step
                    ep = high_prices[i]

            if trend and high_prices[i] > ep or not trend and low_prices[i] < ep:
                acceleration_factor = min(acceleration_factor + step, max_step)

            sar.append(new_sar)

        return Series(sar)