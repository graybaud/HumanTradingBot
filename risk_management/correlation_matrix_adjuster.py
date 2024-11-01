from typing import Dict, Optional
from strategies.signal import Signal
from risk_management import RiskAdjuster

class CorrelationMatrixAdjuster(RiskAdjuster):
    def __init__(self, correlation_threshold: float):
        self.correlation_threshold = correlation_threshold

    def adjust(self, signal: Signal) -> Optional[Dict[str, float]]:
        correlated_assets = [asset for asset, corr in signal.portfolio_correlation.items() if corr > self.correlation_threshold]
        if correlated_assets:
            return {"correlated_assets": correlated_assets}
        return None