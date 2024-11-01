from abc import ABC, abstractmethod
from typing import Dict, Optional
from strategies.signal import Signal

class RiskAdjuster(ABC):
    @abstractmethod
    def adjust(self, signal: Signal) -> Optional[Dict[str, float]]:
        """Applies a risk adjustment to the signal and returns details of the adjustment if any"""
        pass
