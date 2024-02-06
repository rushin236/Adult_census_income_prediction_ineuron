from adult_census.config.configuration import ConfigurationManager
from adult_census.components.prediction import Prediction


class PredictionPipeline:
    def __init__(self) -> None:
        pass

    def main(self, user_input):
        config = ConfigurationManager()
        prediction_config = config.get_prediction_config()
        prediction = Prediction(config=prediction_config)
        model, preprocessor = prediction.get_model_preprocessor()
        user_prediction = prediction.get_prediction(
            user_input=user_input, model=model, preprocessor=preprocessor
        )

        return user_prediction
