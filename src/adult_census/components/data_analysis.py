import os
import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from adult_census.logging import logger
from adult_census.entity import DataAnalysisConfig
from adult_census.utils.common import create_directories

import warnings

warnings.filterwarnings("ignore")


class DataAnalysis:
    def __init__(self, config: DataAnalysisConfig):
        self.config = config

        create_directories([self.config.root_dir, self.config.models_dir])

    def get_raw_data(self):
        local_data_file_path = self.config.local_data_file
        df = pd.read_csv(local_data_file_path, encoding="UTF-8")
        logger.info("Raw Data Loaded Successfully.")

        return df

    def handle_missing_values(self, df: pd.DataFrame):
        df = df.replace("?", np.nan)
        columns_with_nan = ["workclass", "occupation", "native.country"]
        [df[col].fillna(df[col].mode()[0], inplace=True) for col in columns_with_nan]
        logger.info("Missing values handled")

        return df

    def get_important_features(self, df: pd.DataFrame):
        logger.info("feature selection started.")

        cate_col = df.select_dtypes(include="object").columns
        num_col = df.select_dtypes(exclude="object").columns

        df[cate_col] = df[cate_col].apply(LabelEncoder().fit_transform)

        X = df.drop("income", axis=1)
        y = df["income"]

        feat_imp = pd.DataFrame()
        rf = RandomForestClassifier()
        rfe = RFE(estimator=rf, n_features_to_select=10)
        rfe.fit(X, y)
        rf.fit(X, y)
        feat_imp["Feature"] = X.columns
        feat_imp["Imp"] = rfe.support_
        feat_imp["Score"] = np.round(rf.feature_importances_, 2)

        X = X.drop(feat_imp[(feat_imp["Score"] < 0.05)]["Feature"], axis=1)

        cate_col = [col for col in cate_col if col in X.columns]
        num_col = [col for col in num_col if col in X.columns]

        logger.info(
            f"Feature selection completed with selection of these columns: {cate_col + num_col}"
        )

        return num_col, cate_col

    def get_preprocessor(self, num_col, cate_col):
        logger.info("Preprocessor Build Start.")

        cate_pipe = Pipeline([("OneHotEncoder", OneHotEncoder())])

        num_pipe = Pipeline([("StandardScaler", StandardScaler())])

        preprocessor = ColumnTransformer(
            [("num_pipe", num_pipe, num_col), ("cate_pipe", cate_pipe, cate_col)]
        )

        logger.info("Preprocessor Build completed.")

        return preprocessor

    def get_preprocessed_data_and_fitted_preprocessor(
        self, df: pd.DataFrame, preprocessor, num_col, cate_col
    ):
        logger.info("Data transformation started.")

        df = df[num_col + cate_col + ["income"]]
        df["income"] = LabelEncoder().fit_transform(df["income"])

        X = df.drop("income", axis=1)
        preprocessed_data = preprocessor.fit_transform(X)
        preprocessed_data = pd.DataFrame(
            preprocessed_data.toarray(), columns=preprocessor.get_feature_names_out()
        )
        preprocessed_data["income"] = df["income"].values

        logger.info("Data transformation completed.")

        return preprocessed_data, preprocessor

    def save_data_preprocessor(self, preprocessed_data: pd.DataFrame, preprocessor):
        preprocessed_data.to_csv(self.config.preprocessed_data_file, index=False)
        logger.info(f"Transformed data saved to: {self.config.preprocessed_data_file}")
        with open(self.config.preprocessor_file, "wb") as f:
            joblib.dump(preprocessor, f)
            logger.info(f"Preprocessor saved to: {self.config.preprocessor_file}")
