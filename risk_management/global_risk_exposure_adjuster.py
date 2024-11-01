from typing import Dict, Optional
from strategies.signal import Signal
from risk_management import RiskAdjuster

class GlobalRiskExposureAdjuster(RiskAdjuster):
    def __init__(self, max_var: float):
        self.max_var = max_var

    def adjust(self, signal: Signal) -> Optional[Dict[str, float]]:
        portfolio_var = signal.calculate_var()
        if portfolio_var > self.max_var:
            return {"global_var_exceeded": portfolio_var}
        return None