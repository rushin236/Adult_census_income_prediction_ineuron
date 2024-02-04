from adult_census.components.data_validation import DataValidation
from adult_census.config.configuration import ConfigurationManager


class DataValidationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(data_validation_config)
        data_validation.validate_all_file_exist()
