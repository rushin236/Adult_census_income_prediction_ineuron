import os
import joblib
import warnings
import pandas as pd
from adult_census.entity import PredictionConfig

warnings.filterwarnings("ignore")


class Prediction:
    def __init__(self, config: PredictionConfig):
        self.config = config

    def get_model_preprocessor(self):
        try:
            with open(self.config.model_file, "rb") as f:
                model = joblib.load(f)

            with open(self.config.preprocessor_file, "rb") as f:
                preprocessor = joblib.load(f)

            return model, preprocessor
        except Exception as e:
            raise e

    def get_prediction(self, user_input, model, preprocessor):
        try:
            user_input = pd.DataFrame(user_input)
            user_input["age"] = user_input["age"].astype("Int16")
            user_input["education.num"] = user_input["education.num"].astype("Int16")
            user_input["hours.per.week"] = user_input["hours.per.week"].astype("Int16")

            user_input = preprocessor.transform(user_input)

            user_input = pd.DataFrame(
                user_input.toarray(), columns=preprocessor.get_feature_names_out()
            )

            user_prediction = model.predict(user_input)

            return user_prediction

        except Exception as e:
            raise e
