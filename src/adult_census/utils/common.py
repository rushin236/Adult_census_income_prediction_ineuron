import os
from pathlib import Path

import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from adult_census.logging import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """read yaml file and returns

    Args:
        path_to_yaml (Path): Path like input

    Raises:
        valueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: _description_
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loads successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """creating list of directories

    Args:
        path_to_directories (list): list of directories
        verbose (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at : {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """

    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"
