from __future__ import absolute_import
import time
from logging import getLogger
from unittest import TestCase

from upath import getp
from tests.utils import getfp

logger = getLogger()


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

        logger.debug(f"C extension is {python_time/c_ext_time} times faster")
        self.assertEqual(result_python, result_c)

    def test_get_integer_from_path(self):
        result_c = getp({"test": 1}, "test", ".", "test")
        self.assertEqual(result_c, 1)