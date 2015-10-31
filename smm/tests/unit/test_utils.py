# -*- coding: utf-8 -*-
import unittest
import os
import mock
from smm.utils import get_env
from smm.utils import get_abs_path
from smm.utils import check_configuration


class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._home = os.path.expanduser('~')
        cls._cwd = os.getcwd()

    def test_get_abs_path(self):
        """Get Linux absolute path"""
        test_cases = {
            "~": self._home,
            "tmp/dir/my_dir": os.path.join(self._cwd, "tmp/dir/my_dir"),
            "/tmp/test": "/tmp/test",
            "~/.mydir": os.path.join(self._home, ".mydir")
        }
        for key, value in test_cases.iteritems():
            self.assertEqual(os.path.normpath(get_abs_path(key)),
                             os.path.normpath(value)
                             )

    @mock.patch('smm.utils.os')
    def test_get_env(self, mock_os):
        """Get Linux env_variable value"""
        def_value = '42'
        test_data = {"my_test_key_1": "my_test_value_1",
                     "fake_path": "fake_path_value",
                     "empty_env": " "}
        test_results = ["my_test_value_1", "fake_path_value", def_value]

        # Mock os.environ
        mock_os.environ = test_data

        test_cases_keys = test_data.keys()
        test_cases_keys.append(
            "SHOULD_BE_NONEXISTENT_VARIABLE_FOR_SMM_TESTING_ONLY")
        test_results.append(def_value)

        for index, key in enumerate(test_cases_keys):
            self.assertEqual(get_env(key, def_value), test_results[index])

    def test_check_configuration(self):
        """Check DB path and access rights"""
        self.assertFalse(
            check_configuration('this_path/should_not_be/valid/but_you/never/know'))
        if os.name.lower() in ('posix', 'mac'):
            self.assertTrue(check_configuration('/tmp/'))
