from typing import Dict, Optional
from strategies.signal import Signal
from risk_management import RiskAdjuster

class VolatilityBasedStopLossAdjuster(RiskAdjuster):
    def __init__(self, atr_multiplier: float):
        self.atr_multiplier = atr_multiplier

    def adjust(self, signal: Signal) -> Optional[Dict[str, float]]:
        adjusted_stop_loss = signal.entry_price - self.atr_multiplier * signal.atr
        if adjusted_stop_loss < signal.stop_loss:
            return {"adjusted_stop_loss": adjusted_stop_loss}
        return None