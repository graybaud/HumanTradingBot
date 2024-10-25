import pandas as pd
import logging
import Indicators

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, indicators):
        self.indicators = indicators

    def enrich_klines_with_indicators(self, df):
        df['ema_14'] = Indicators.ema(df['close'], period=14)
        df['macd_line'], df['signal_line'] = Indicators.macd(df['close'])
        df['stoch_k'], df['stoch_d'] = Indicators.stochastique(df['high'], df['low'], df['close'])
        df['rsi'] = Indicators.rsi(df['close'], period=14)
        df['upper_band'], df['middle_band'], df['lower_band'] = Indicators.bollinger_bands(df['close'])
        df['volume_profile'] = Indicators.volume_profile(df['close'])
        df['sma_50'] = Indicators.sma(df['close'], period=50)
        df['sar'] = Indicators.parabolic_sar(df['high'], df['low'], df['close'])
        # TO BE DONE later
        # df['sentiment'] = Indicators.sentiment('symbol', external_data)  # Remplacer par les données externes appropriées
        df['fractals_high'], df['fractals_low'] = Indicators.fractals(df['high'], df['low'])
        df['atr'] = Indicators.atr(df['high'], df['low'], df['close'], period=14)
        df['upper_keltner'], df['middle_keltner'], df['lower_keltner'] = Indicators.keltner_channels(df['close'], df['high'], df['low'])
        df['cci'] = Indicators.cci(df['high'], df['low'], df['close'], period=20)
        df['fib_ext'] = Indicators.fibonacci_extensions(df['high'], df['low'])
        df['fib_retr'] = Indicators.fibonacci_retracement(df['high'], df['low'])
        df['pivot'], df['resistance_1'], df['support_1'] = Indicators.pivot_points(df['high'], df['low'], df['close'])
        df['support'], df['resistance'] = Indicators.support_resistance(df['high'], df['low'])
        df['multi_timeframe'] = Indicators.multi_timeframe_analysis([df])  # Assurez-vous de fournir une liste de DataFrames
        df['vwap'] = Indicators.vwap(df['close'], df['volume'])
        df['adx'] = Indicators.adx(df['high'], df['low'], df['close'], period=14)
        df['psychological_levels'] = Indicators.psychological_levels(df['close'])
        df['tenkan'], df['kijun'], df['senkou_a'], df['senkou_b'], df['chikou'] = Indicators.ichimoku_cloud(df['high'], df['low'], df['close'])

        return df
