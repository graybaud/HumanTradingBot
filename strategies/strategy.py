from pandas import DataFrame 
from logging import get_logger

logger = get_logger(__name__)

class Strategy:
    def __init__(self, name, config, df):
        self.name = name
        self.config = config  # Dictionnaire de configuration propre à chaque stratégie
        self.df = df  # DataFrame contenant les données de marché

    def generate_signal(self):
        raise NotImplementedError("Cette méthode doit être implémentée dans les sous-classes.")

    # def log_signal(self, signal):
    #     logger.info(f"Signal généré par la stratégie {self.name}: {signal}")


