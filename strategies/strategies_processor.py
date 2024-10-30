from pandas import DataFrame 
from logging import get_logger

logger = get_logger(__name__)

class StrategiesProcessor:
    def __init__(self, strategies):
        self.strategies = strategies

    def process(self, df):
        """
        Appliquer toutes les stratégies sur le DataFrame et retourner les actions recommandées.
        """
        # recommendations = {}
        all_signals = []

        for strategy in self.strategies:
            signal = strategy.generate_signal(df)
            if signal:
                #strategy.log_signal(signal)
                # all_signals.append(signal)
                all_signals[strategy.name] = signal

        # Filtrage ou pondération des signaux si nécessaire
        #validated_signals = self.filter_signals(all_signals)
        return all_signals

    def filter_signals(self, signals):
        """
        Filtrer et valider les signaux en fonction de critères personnalisés.
        """
        # Ex: Ne garder que les signaux avec un niveau de confiance supérieur à un certain seuil
        return [signal for signal in signals if signal.confidence >= 0.7]
