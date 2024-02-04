from adult_census.components.model_build import (
    ModelBuild,
    get_train_test_split,
    get_report,
    get_models,
)
from adult_census.config.configuration import ConfigurationManager


class ModelBuildPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_build_config, params = config.get_model_build_config()
        model_build = ModelBuild(config=model_build_config, params=params)
        df, preprocessor = model_build.get_data_preprocessor()
        train_test_set = get_train_test_split(df=df)
        models = get_models()
        tr_models, tr_results = model_build.train_model(
            models_dict=models, X_train=train_test_set[0], y_train=train_test_set[2]
        )
        tr_results = get_report(result=tr_results)
        hy_models, hy_results = model_build.train_model(
            models_dict=models,
            X_train=train_test_set[0],
            y_train=train_test_set[2],
            parameters=True,
        )
        hy_results = get_report(result=hy_results)
        best_model = model_build.get_best_model(hy_models, hy_results)
        model_build.save_results(
            {"Trained Models": tr_results, "Tunned Models": hy_results}
        )
        model_build.save_model(best_model)
