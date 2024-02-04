from adult_census.constants import *
from adult_census.utils.common import read_yaml, create_directories

from adult_census.entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataAnalysisConfig,
    ModelBuildConfig,
)


class ConfigurationManager:
    def __init__(
        self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH
    ) -> None:
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
        )

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,
        )

        return data_validation_config

    def get_data_analysis_config(self) -> DataAnalysisConfig:
        config = self.config.data_analysis

        data_analysis_config = DataAnalysisConfig(
            root_dir=config.root_dir,
            models_dir=config.models_dir,
            local_data_file=config.local_data_file,
            preprocessed_data_file=config.preprocessed_data_file,
            preprocessor_file=config.preprocessor_file,
        )

        return data_analysis_config

    def get_model_build_config(self) -> ModelBuildConfig:
        config = self.config.model_build

        model_build_config = ModelBuildConfig(
            root_dir=config.root_dir,
            preprocessed_data_file=config.preprocessed_data_file,
            preprocessor_file=config.preprocessor_file,
            model_file=config.model_file,
            model_results=config.model_results,
            best_params=config.best_params,
        )

        return model_build_config, self.params
