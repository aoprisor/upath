from logging import getLogger
from typing import Union, List, Dict, Any

logger = getLogger(__name__)


def getfp(nested_input: Union[List, Dict], path: Union[str, list], separator: str = '.', default_value=None) -> Any:
    """
    get value from dict path
    :param nested_input
    :param path:
    :param separator:
    :param default_value:
    :return:
    """
    path_list = path if isinstance(path, list) else path.split(separator)

    current_val = nested_input

    for key in path_list:
        try:
            if key.isdecimal() and isinstance(current_val, list):
                if int(key) < len(current_val):
                    key = int(key)
                else:
                    logger.info(
                        f"Can't retrieve value from list in path {path}, key {key}, list index out of range")
                    return default_value

            current_val = current_val[key]
        except KeyError:
            logger.info(f"Can't retrieve value from dict in path {path}, key {key}, key not found")
            return default_value
        except TypeError:
            logger.info(f"Path {path} can't be resolved, stuck at key {key}")
            return default_value

    return current_val
