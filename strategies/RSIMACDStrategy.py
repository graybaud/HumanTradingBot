from strategies.strategy import Strategy
from strategies.signal import Signal

class RSIMACDStrategy(Strategy):
    def __init__(self, rsi_threshold_buy=30, rsi_threshold_sell=70, macd_signal_threshold=0):
        self.rsi_threshold_buy = rsi_threshold_buy
        self.rsi_threshold_sell = rsi_threshold_sell
        self.macd_signal_threshold = macd_signal_threshold

    def generate_signal(self, df):
        """
        Génère un signal en fonction des indicateurs RSI et MACD.
        df : DataFrame contenant les données historiques et les valeurs indicateurs.
        """

        # Récupération des dernières valeurs des indicateurs RSI et MACD
        latest_rsi = df['rsi'].iloc[-1]
        macd_line = df['macd_line'].iloc[-1]
        signal_line = df['signal_line'].iloc[-1]
        macd_diff = macd_line - signal_line  # MACD Histogramme
        
        # Initialisation des variables du signal
        signal_type = None
        confidence = 0.5  # Confiance de base

        # Détection du signal en fonction des indicateurs
        if latest_rsi < self.rsi_threshold_buy and macd_diff > self.macd_signal_threshold:
            signal_type = 'Buy'
            confidence += 0.2  # Augmente la confiance pour cette configuration
        elif latest_rsi > self.rsi_threshold_sell and macd_diff < -self.macd_signal_threshold:
            signal_type = 'Sell'
            confidence += 0.2  # Augmente la confiance pour cette configuration
        else:
            signal_type = 'Hold'
            confidence -= 0.1  # Pas de signal fort

        # Définition des niveaux de stop-loss et take-profit basés sur les derniers prix
        entry_price = df['close'].iloc[-1]
        stop_loss = entry_price * (0.98 if signal_type == 'Buy' else 1.02)
        take_profit = entry_price * (1.04 if signal_type == 'Buy' else 0.96)

        # Volume suggéré en pourcentage du capital total
        suggested_volume = 0.1  # Par défaut à 10% du capital

        # Création du signal avec les paramètres initiaux
        signal = Signal(
            type=signal_type,
            symbol=df['symbol'].iloc[-1],
            timeframe=df['timeframe'].iloc[-1],
            confidence=confidence,
            suggested_volume=suggested_volume,
            stop_loss=stop_loss,
            take_profit=take_profit,
            validity_period=timedelta(hours=1)  # Durée de validité du signal
        )

        return signal
