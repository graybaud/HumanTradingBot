from datetime import datetime
from enum import Enum
from typing import Dict, Optional


class ActionType(Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    HOLD = 'HOLD'
    NOT = 'NOTHING'


class Signal:
    def __init__(self, signal_id: str, action: ActionType, symbol: str, timeframe: str,
                 confidence: float, suggested_volume: float, stop_loss: float, 
                 take_profit: float, validity_duration: int, additional_info: Optional[Dict] = None):
        self.signal_id = signal_id  # ID unique du signal pour le suivi et la traçabilité
        self.action = action  # Action recommandée (achat, vente ou maintien)
        self.symbol = symbol  # Actif concerné (ex : 'BTC/USD')
        self.timeframe = timeframe  # Délai sur lequel le signal a été généré
        self.confidence = confidence  # Score ou évaluation de la fiabilité du signal
        self.suggested_volume = suggested_volume  # Montant ou pourcentage recommandé
        self.stop_loss = stop_loss  # Niveau de stop loss recommandé
        self.take_profit = take_profit  # Niveau de take profit recommandé
        self.validity_duration = validity_duration  # Durée de validité du signal (en minutes, par ex.)
        self.timestamp = datetime.now()  # Horodatage du signal
        self.additional_info = additional_info if additional_info else {}  # Infos contextuelles supplémentaires

    def is_valid(self) -> bool:
        """Vérifie si le signal est encore valide en fonction de la durée de validité."""
        elapsed_time = datetime.now() - self.timestamp
        return elapsed_time.total_seconds() <= self.validity_duration * 60
