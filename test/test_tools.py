import textwrap
import unittest

from tools import is_code_valid


class TestMcpTools(unittest.TestCase):

    def test_is_code_valid_none(self):
        valid, error_msg = is_code_valid("")
        self.assertTrue(valid)
        self.assertIsNone(error_msg)
        #
        valid, error_msg = is_code_valid("  ")
        self.assertTrue(valid)
        self.assertIsNone(error_msg)

    def test_is_code_valid_ko(self):
        valid, error_msg = is_code_valid("if foo")
        self.assertFalse(valid)
        print(error_msg)
        self.assertTrue("Traceback" in error_msg)
        self.assertTrue("ast.parse(code)" in error_msg)

    def test_is_code_valid_ok(self):
        valid, error_msg = is_code_valid("print ('Hello, World!')")
        self.assertTrue(valid)
        self.assertIsNone(error_msg)
        #
        code="""
        from math import sqrt
        from random import random
        x=random() + sqrt(2)
        print(x)
        """
        code = textwrap.dedent(code)
        valid, error_msg = is_code_valid(code)
        print(error_msg)
        self.assertTrue(valid)
        self.assertIsNone(error_msg)
