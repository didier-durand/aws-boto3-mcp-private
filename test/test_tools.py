import asyncio
import textwrap
import unittest


from tools import is_code_valid, is_deno_installed, execute_code


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

    def test_is_deno_installed(self):
        installed, stdout = is_deno_installed()
        print(stdout)
        self.assertTrue(installed)
        self.assertTrue("deno" in stdout)
        self.assertTrue("typescript" in stdout)
        #
        installed, stdout = is_deno_installed(command="foo-bar-boo")
        self.assertFalse(installed)
        self.assertEqual("",stdout)


    def test_execute_code(self):
        code = """
        import numpy
        a = numpy.array([1, 2, 3])
        print(a)
        a
        """
        #
        is_error, log = asyncio.run(execute_code(code=code,debug=True))
        self.assertFalse(is_error)
        print(log)
