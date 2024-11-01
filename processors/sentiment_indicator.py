from processors import Indicator

class SentimentIndicator(Indicator):
    def compute(self, *args, **kwargs):
        symbol = kwargs.get('symbol')
        external_data = kwargs.get('external_data')
        sentiment_value = external_data.get_sentiment(symbol)
        return sentiment_value