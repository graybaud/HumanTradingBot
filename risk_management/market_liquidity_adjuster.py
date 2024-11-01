from typing import Dict, Optional
from strategies.signal import Signal
from risk_management import RiskAdjuster

class MarketLiquidityAdjuster(RiskAdjuster):
    def __init__(self, min_liquidity: float):
        self.min_liquidity = min_liquidity

    def adjust(self, signal: Signal) -> Optional[Dict[str, float]]:
        if signal.market_liquidity < self.min_liquidity:
            adjusted_position_size = signal.position_size * 0.5
            return {"reduced_position_due_to_liquidity": adjusted_position_size}
        return None