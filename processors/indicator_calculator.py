from pandas import Series, concat, cut
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Indicators:
    @staticmethod
    def ema(close_prices, period=14):
        return close_prices.ewm(span=period, adjust=False).mean()

    @staticmethod
    def macd(close_prices, short_period=12, long_period=26, signal_period=9):
        short_ema = close_prices.ewm(span=short_period, adjust=False).mean()
        long_ema = close_prices.ewm(span=long_period, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        return macd_line, signal_line

    @staticmethod
    def stochastique(high_prices, low_prices, close_prices, k_period=14, d_period=3):
        low_k = low_prices.rolling(window=k_period).min()
        high_k = high_prices.rolling(window=k_period).max()
        k_value = 100 * (close_prices - low_k) / (high_k - low_k)
        d_value = k_value.rolling(window=d_period).mean()
        return k_value, d_value

    @staticmethod
    def rsi(close_prices, period=14):
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def bollinger_bands(close_prices, period=20, std_dev=2):
        sma = close_prices.rolling(window=period).mean()
        rolling_std = close_prices.rolling(window=period).std()
        upper_band = sma + (rolling_std * std_dev)
        lower_band = sma - (rolling_std * std_dev)
        return upper_band, sma, lower_band
    
    @staticmethod
    def volume_profile(close_prices, bins=10):
        volume_profile = cut(close_prices, bins=bins).value_counts()
        return volume_profile


    @staticmethod
    def sma(close_prices, period=14):
        return close_prices.rolling(window=period).mean()


    @staticmethod
    def parabolic_sar(high_prices, low_prices, close_prices, step=0.02, max_step=0.2):
        sar = [close_prices[0]]
        ep = high_prices[0]
        acceleration_factor = step
        trend = True
        
        for i in range(1, len(close_prices)):
            new_sar = sar[i - 1] + acceleration_factor * (ep - sar[i - 1])
            ep = max(ep, high_prices[i]) if trend else min(ep, low_prices[i])
            
            if trend:
                new_sar = min(new_sar, low_prices[i], low_prices[i - 1])
                if low_prices[i] < new_sar:
                    trend = False
                    acceleration_factor = step
                    ep = low_prices[i]
            else:
                new_sar = max(new_sar, high_prices[i], high_prices[i - 1])
                if high_prices[i] > new_sar:
                    trend = True
                    acceleration_factor = step
                    ep = high_prices[i]
            
            if trend and high_prices[i] > ep or not trend and low_prices[i] < ep:
                acceleration_factor = min(acceleration_factor + step, max_step)
            
            sar.append(new_sar)
        
        return Series(sar)


    @staticmethod
    def sentiment(symbol, external_data):
        sentiment_value = external_data.get_sentiment(symbol)
        return sentiment_value


    @staticmethod
    def fractals(high_prices, low_prices, period=5):
        high_fractal = (high_prices == high_prices.rolling(window=period, center=True).max())
        low_fractal = (low_prices == low_prices.rolling(window=period, center=True).min())
        return high_fractal, low_fractal


    @staticmethod
    def atr(high_prices, low_prices, close_prices, period=14):
        high_low = high_prices - low_prices
        high_close = (high_prices - close_prices.shift()).abs()
        low_close = (low_prices - close_prices.shift()).abs()
        true_range = concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        return atr


    @staticmethod
    def keltner_channels(close_prices, high_prices, low_prices, period=20, atr_mult=2):
        ema = close_prices.ewm(span=period, adjust=False).mean()
        atr = Indicators.atr(high_prices, low_prices, close_prices, period=period)
        upper_band = ema + (atr_mult * atr)
        lower_band = ema - (atr_mult * atr)
        return upper_band, ema, lower_band


    @staticmethod
    def cci(high_prices, low_prices, close_prices, period=20):
        typical_price = (high_prices + low_prices + close_prices) / 3
        sma = typical_price.rolling(window=period).mean()
        mean_deviation = (typical_price - sma).abs().rolling(window=period).mean()
        cci = (typical_price - sma) / (0.015 * mean_deviation)
        return cci


    @staticmethod
    def fibonacci_extensions(high_prices, low_prices, levels=[0.236, 0.382, 0.618, 0.5, 0.786, 1.0]):
        price_diff = high_prices.max() - low_prices.min()
        extensions = {level: high_prices.max() + price_diff * level for level in levels}
        return extensions


    @staticmethod
    def fibonacci_retracement(high_prices, low_prices, levels=[0.236, 0.382, 0.618, 0.5, 0.786, 1.0]):
        price_diff = high_prices.max() - low_prices.min()
        retracements = {level: high_prices.max() - price_diff * level for level in levels}
        return retracements


    @staticmethod
    def pivot_points(high_prices, low_prices, close_prices):
        pivot = (high_prices + low_prices + close_prices) / 3
        resistance_1 = (2 * pivot) - low_prices
        support_1 = (2 * pivot) - high_prices
        return pivot, resistance_1, support_1

    @staticmethod
    def support_resistance(high_prices, low_prices, period=20):
        support = low_prices.rolling(window=period).min()
        resistance = high_prices.rolling(window=period).max()
        return support, resistance


    @staticmethod
    def multi_timeframe_analysis(df_list):
        # df_list contient les DataFrames pour chaque timeframe
        combined_data = concat(df_list, axis=1)
        return combined_data


    @staticmethod
    def vwap(close_prices, volumes):
        return (volumes * close_prices).cumsum() / volumes.cumsum()
    
    @staticmethod
    def adx(high_prices, low_prices, close_prices, period=14):
        up_move = high_prices.diff()
        down_move = low_prices.diff()
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        atr = Indicators.atr(high_prices, low_prices, close_prices, period=period)
        plus_di = 100 * (Series(plus_dm).rolling(window=period).mean() / atr)
        minus_di = 100 * (Series(minus_dm).rolling(window=period).mean() / atr)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        adx = dx.rolling(window=period).mean()
        return adx


    @staticmethod
    def psychological_levels(close_prices):
        return close_prices.apply(lambda x: round(x, -len(str(int(x))) + 1))

    @staticmethod
    def ichimoku_cloud(high_prices, low_prices, close_prices, period_tenkan=9, period_kijun=26, period_senkou=52):
        tenkan_sen = (high_prices.rolling(window=period_tenkan).max() + low_prices.rolling(window=period_tenkan).min()) / 2
        kijun_sen = (high_prices.rolling(window=period_kijun).max() + low_prices.rolling(window=period_kijun).min()) / 2
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(period_kijun)
        senkou_span_b = ((high_prices.rolling(window=period_senkou).max() + low_prices.rolling(window=period_senkou).min()) / 2).shift(period_kijun)
        chikou_span = close_prices.shift(-period_kijun)
        return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span
