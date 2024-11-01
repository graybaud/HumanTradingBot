from processors import Indicator
from pandas import concat

class MultiTimeframeAnalysisIndicator(Indicator):
    def compute(self, *args, **kwargs):
        df_list = kwargs.get('df_list')
        # df_list contains DataFrames for each timeframe
        combined_data = concat(df_list, axis=1)
        return combined_data