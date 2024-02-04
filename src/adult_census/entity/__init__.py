from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: Path
    ALL_REQUIRED_FILES: str


@dataclass
class DataAnalysisConfig:
    root_dir: Path
    models_dir: Path
    local_data_file: Path
    preprocessed_data_file: Path
    preprocessor_file: Path


@dataclass
class ModelBuildConfig:
    root_dir: Path
    preprocessed_data_file: Path
    preprocessor_file: Path
    model_file: Path
    model_results: Path
    best_params: Path
