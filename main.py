from adult_census.logging import logger
from adult_census.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from adult_census.pipeline.stage_02_data_validation import DataValidationPipeline
from adult_census.pipeline.stage_03_data_analysis import DataAnalysisPipeline
from adult_census.pipeline.stage_04_model_build import ModelBuildPipeline

import warnings

warnings.filterwarnings("ignore")

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>{STAGE_NAME} started <<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n\nx============x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Validation Stage"
try:
    logger.info(f">>>>>{STAGE_NAME} started <<<<<")
    data_validation = DataValidationPipeline()
    data_validation.main()
    logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n\nx============x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Analysis Stage"
try:
    logger.info(f">>>>>{STAGE_NAME} started <<<<<")
    data_analysis = DataAnalysisPipeline()
    data_analysis.main()
    logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n\nx============x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Build Stage"
try:
    logger.info(f">>>>>{STAGE_NAME} started <<<<<")
    model_build = ModelBuildPipeline()
    model_build.main()
    logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n\nx============x")
except Exception as e:
    logger.exception(e)
    raise e
