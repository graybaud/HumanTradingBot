from typing import Dict, Optional
from strategies.signal import Signal
from risk_management import RiskAdjuster

class RiskRewardRatioAdjuster(RiskAdjuster):
    def __init__(self, min_ratio: float, atr_multiplier: float):
        self.min_ratio = min_ratio
        self.atr_multiplier = atr_multiplier

    def adjust(self, signal: Signal) -> Optional[Dict[str, float]]:
        target_profit = signal.entry_price + self.atr_multiplier * signal.atr
        rr_ratio = target_profit / abs(signal.stop_loss)
        if rr_ratio >= self.min_ratio:
            return {"dynamic_rr_ratio": rr_ratio, "adjusted_target_profit": target_profit}
        return None