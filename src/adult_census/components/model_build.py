import os
import warnings

warnings.filterwarnings("ignore")

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
)
from xgboost import XGBClassifier

from adult_census.logging import logger
from adult_census.utils.common import create_directories
from adult_census.entity import ModelBuildConfig


class ModelBuild:
    def __init__(self, config: ModelBuildConfig, params):
        self.config = config
        self.params = params

        create_directories([self.config.root_dir])

    def get_data_preprocessor(self):
        logger.info("Loading transformed data and preprocessor.")

        df = pd.read_csv(self.config.preprocessed_data_file)

        with open(self.config.preprocessor_file, "rb") as f:
            preprocessor = joblib.load(f)

        logger.info("Transformed data and Preprocessor loading complete.")

        return df, preprocessor

    def train_model(self, models_dict, X_train, y_train, parameters: bool = False):
        try:
            tr_models = {}
            tr_results = {}

            for model in models_dict.keys():
                if (parameters == True) and (model in self.params.keys()):
                    logger.info(f"Hyperparameter tuning for {model} started.")
                    parameter_of_model = self.params[model]
                    tr_model, result, best_params = fit_model(
                        models_dict[model],
                        X_train,
                        y_train,
                        parameters=parameter_of_model,
                    )

                    logger.info(f"Hyperparameter tuning for {model} completed.")

                    if (best_params != None) and (
                        not os.path.exists(self.config.best_params)
                    ):
                        with open(self.config.best_params, "w") as f:
                            f.write(f"Best Params for {model}: \n {best_params}")
                    else:
                        with open(self.config.best_params, "a") as f:
                            f.write(f"\n\nBest Params for {model}: \n {best_params}")
                else:
                    logger.info(f"Model training for {model} started.")
                    tr_model, result = fit_model(models_dict[model], X_train, y_train)
                    logger.info(f"Model training for {model} completed.")

                tr_models[model] = tr_model
                tr_results[model] = result

            return tr_models, tr_results
        except Exception as e:
            raise e

    def get_best_model(self, models_dict: dict, models_results: pd.DataFrame):
        best_model = models_results.sort_values("accuracy", ascending=False)[
            "models"
        ].to_list()[0]
        best_model = models_dict[best_model]
        return best_model

    def save_results(self, results: dict):
        try:
            for result in results.keys():
                res = results[result]
                if not os.path.exists(self.config.model_results):
                    with open(self.config.model_results, "w") as f:
                        f.write(
                            f"Results for {result}: \n{res.sort_values('accuracy', ascending=False).to_string()}"
                        )
                else:
                    with open(self.config.model_results, "a") as f:
                        f.write(
                            f"\nResults for {result}: \n{res.sort_values('accuracy', ascending=False).to_string()}"
                        )

            logger.info(f"Model results saved to {self.config.model_results}")
        except Exception as e:
            raise e

    def save_model(self, model):
        try:
            with open(self.config.model_file, "wb") as f:
                joblib.dump(model, f)
                logger.info(f"Model saved to {self.config.model_file}")
        except Exception as e:
            raise e


# helper functions for model training and evaluation


def fit_model(model, x, y, parameters=None):
    try:
        if parameters != None:
            gcv = GridSearchCV(estimator=model, param_grid=parameters, n_jobs=-1)
            gcv.fit(X=x, y=y)
            best_params = gcv.best_params_
            model.set_params(**gcv.best_params_)
            pred = model.predict(x)
            result = classification_report(y, pred, output_dict=True)
            return model, result, best_params
        else:
            model.fit(x, y)
            pred = model.predict(x)
            result = classification_report(y, pred, output_dict=True)
            return model, result
    except Exception as e:
        raise e


def get_models():
    models_dict = {
        "LogisticRegression": LogisticRegression(),
        "SVC": SVC(),
        "KNeighborsClassifier": KNeighborsClassifier(),
        "GaussianNB": GaussianNB(),
        "DecisionTreeClassifier": DecisionTreeClassifier(),
        "RandomForestClassifier": RandomForestClassifier(),
        "AdaBoostClassifier": AdaBoostClassifier(),
        "GradientBoostingClassifier": GradientBoostingClassifier(),
        "XGBClassifier": XGBClassifier(),
    }

    return models_dict


def get_train_test_split(df: pd.DataFrame):
    X = df.drop("income", axis=1)
    y = df["income"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return [X_train, X_test, y_train, y_test]


def get_report(result: dict):
    cr = {}
    cr["models"] = []
    cr["accuracy"] = []
    cr["macro avg precision"] = []
    cr["macro avg recall"] = []
    cr["macro avg f1-score"] = []
    cr["weighted avg precision"] = []
    cr["weighted avg recall"] = []
    cr["weighted avg f1-score"] = []
    for i, model in enumerate(result.keys()):
        cr["models"].append(model)
        cr["accuracy"].append(round(result[model]["accuracy"], 2))
        cr["macro avg precision"].append(
            round(result[model]["macro avg"]["precision"], 2)
        )
        cr["macro avg recall"].append(round(result[model]["macro avg"]["recall"], 2))
        cr["macro avg f1-score"].append(
            round(result[model]["macro avg"]["f1-score"], 2)
        )
        cr["weighted avg precision"].append(
            round(result[model]["weighted avg"]["precision"], 2)
        )
        cr["weighted avg recall"].append(
            round(result[model]["weighted avg"]["recall"], 2)
        )
        cr["weighted avg f1-score"].append(
            round(result[model]["weighted avg"]["f1-score"], 2)
        )
        target_class = result[model].keys()
        for each in target_class:
            if each not in ["accuracy", "macro avg", "weighted avg"]:
                if i == 0:
                    cr[each + " " + "precision"] = []
                    cr[each + " " + "recall"] = []
                    cr[each + " " + "f1-score"] = []

                cr[each + " " + "precision"].append(
                    round(result[model][each]["precision"], 2)
                )
                cr[each + " " + "recall"].append(
                    round(result[model][each]["recall"], 2)
                )
                cr[each + " " + "f1-score"].append(
                    round(result[model][each]["f1-score"], 2)
                )

    return pd.DataFrame(cr)
