from __future__ import absolute_import

import time
from logging import getLogger
from typing import Union, List, Dict, Any
from unittest import TestCase

from upath import getp

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


class GetFromPathTests(TestCase):
    """
    basic tests
    """

    def nest_dict(self, dict_to_nest: dict, level: int, key_prefix: str, path: str):
        """
        generate a nested structure
        :param dict_to_nest:
        :param level:
        :param key_prefix:
        :param path:
        :return:
        """
        if level == 0:
            return path

        dict_to_nest[key_prefix + str(level)] = {}
        path += "." + key_prefix + str(level) if path else key_prefix + str(level)

        return self.nest_dict(dict_to_nest[key_prefix + str(level)], level - 1, key_prefix, path)

    def test_both_versions_give_the_same_results_and_display_speed_comparison(self):
        nested_dict = {}
        path = self.nest_dict(nested_dict, 100, "path", "")

        now = time.time()
        result_c = getp(nested_dict, path)
        c_ext_time = time.time() - now

        now = time.time()
        result_python = getfp(nested_dict, path)
        python_time = time.time() - now

        logger.error(f"C extension is {python_time / c_ext_time} times faster")
        self.assertEqual(result_python, result_c)

    def test_get_integer_from_path(self):
        result_c = getp({"test": 1}, "test")
        self.assertEqual(result_c, 1)

    def test_get_from_path_with_list(self):
        result_c = getp({"test": {"test2": [{"test3": 1}]}}, "test.test2.0.test3")
        self.assertEqual(result_c, 1)

    def test_get_from_path_with_different_separator(self):
        result_c = getp({"test": {"test.2": [{"test3": 1}]}}, "test/test.2/0/test3", "/")
        self.assertEqual(result_c, 1)

    def test_path_not_found_set_default(self):
        result_c = getp({"test": {"test2": [{"test3": 7}]}}, "test/test.2/0/test3", "/", 1)
        self.assertEqual(result_c, 1)

    def test_no_arguments_raises_exception(self):
        with self.assertRaises(Exception):
            getp()

    def test_one_argument_raises_exception(self):
        with self.assertRaises(Exception):
            getp({"test": 2})
