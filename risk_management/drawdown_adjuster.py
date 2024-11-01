from typing import Dict, Optional
from strategies.signal import Signal
from risk_management import RiskAdjuster

class DrawdownAdjuster(RiskAdjuster):
    def __init__(self, max_drawdown: float):
        self.max_drawdown = max_drawdown

    def adjust(self, signal: Signal) -> Optional[Dict[str, float]]:
        if signal.current_drawdown >= self.max_drawdown:
            return {"drawdown_threshold_met": signal.current_drawdown}
        return None
