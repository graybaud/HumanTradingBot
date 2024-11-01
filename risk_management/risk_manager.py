from typing import List, Optional
from strategies.signal import Signal

from risk_management import RiskAdjuster

class RiskManager:
    def __init__(self, adjusters: List[RiskAdjuster]):
        self.adjusters = adjusters

    def process_signal(self, signal: Signal, cache_manager) -> Optional[Signal]:
        adjustments = []

        # Appliquer chaque ajusteur
        for adjuster in self.adjusters:
            adjustment = adjuster.adjust(signal)
            if adjustment:
                adjustments.append(adjustment)

        # Sauvegarde des ajustements pour traçabilité
        cache_manager.save_signal_with_risk(signal, adjustments)

        return signal if adjustments else None
