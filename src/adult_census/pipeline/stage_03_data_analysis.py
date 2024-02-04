from adult_census.components.data_analysis import DataAnalysis
from adult_census.config.configuration import ConfigurationManager


class DataAnalysisPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_analysis_config = config.get_data_analysis_config()
        data_analysis = DataAnalysis(data_analysis_config)
        df = data_analysis.get_raw_data()
        df1 = df.copy()
        df2 = data_analysis.handle_missing_values(df1)
        num_col, cate_col = data_analysis.get_important_features(df2)
        preprocessor = data_analysis.get_preprocessor(
            num_col=num_col, cate_col=cate_col
        )
        transformed_data, preprocessor = (
            data_analysis.get_preprocessed_data_and_fitted_preprocessor(
                df=df, preprocessor=preprocessor, num_col=num_col, cate_col=cate_col
            )
        )
        data_analysis.save_data_preprocessor(
            preprocessed_data=transformed_data, preprocessor=preprocessor
        )
