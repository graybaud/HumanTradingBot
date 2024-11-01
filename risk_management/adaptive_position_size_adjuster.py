from typing import Dict, Optional
from strategies.signal import Signal
from risk_management import RiskAdjuster

class AdaptivePositionSizeAdjuster(RiskAdjuster):
    def __init__(self, capital: float, risk_per_trade: float):
        self.capital = capital
        self.risk_per_trade = risk_per_trade

    def adjust(self, signal: Signal) -> Optional[Dict[str, float]]:
        position_size = (self.capital * self.risk_per_trade) / (self.atr_multiplier * signal.atr)
        return {"adaptive_position_size": position_size}