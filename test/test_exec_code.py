import asyncio
import textwrap

from mcp_testcase import McpTestCase  # pylint: disable=E0401
from tools import is_code_valid, is_deno_installed, execute_code, process_execution_log


class TestMcpTools(McpTestCase):

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
        code = """
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
        self.assertEqual("", stdout)

    def test_execute_code_ok(self):
        code = """
        import numpy
        a = numpy.array([1, 2, 3])
        print(a)
        a
        """
        #
        is_error, log = asyncio.run(execute_code(code=code, debug=False))
        self.assertFalse(is_error)
        print(f"\nexecution log:\n{log}")
        self.assertTrue("status" in log)
        self.assertTrue("dependencies" in log)
        self.assertTrue("[1 2 3]" in log)
        status, exec_result, dependencies = process_execution_log(log=log)
        self.assertEqual("success", status)
        self.assertTrue("[1 2 3]" in exec_result)
        self.assertEqual(["numpy"], dependencies)

    def test_execute_syntax_error(self):
        # missing numpy import
        code = """
        if x == 1
        """
        is_error, log = asyncio.run(execute_code(code=code, debug=False))
        print(f"\nexecution log:\n{log}")
        self.assertFalse(is_error)
        self.assertTrue("SyntaxError" in log)
        status, exec_result, dependencies = process_execution_log(log=log)
        self.assertEqual("run-error", status)
        self.assertTrue("SyntaxError" in exec_result)
        self.assertEqual([], dependencies)

    def test_execute_name_error(self):
        # missing numpy import
        code = """
        a = numpy.array([1, 2, 3])
        """
        is_error, log = asyncio.run(execute_code(code=code, debug=False))
        print(f"\nexecution log:\n{log}")
        self.assertFalse(is_error)
        self.assertTrue("NameError" in log)
        status, exec_result, dependencies = process_execution_log(log=log)
        self.assertEqual("run-error", status)
        self.assertTrue("NameError" in exec_result)
        self.assertEqual([], dependencies)

    def test_execute_code_div_by_zero(self):
        code = """
        import math
        x = math.sqrt(2)
        y = 0
        x / y
        """
        is_error, log = asyncio.run(execute_code(code=code, debug=False))
        print(f"\nexecution log:\n{log}")
        self.assertFalse(is_error)
        self.assertTrue("ZeroDivisionError" in log)
        status, exec_result, dependencies = process_execution_log(log=log)
        self.assertEqual("run-error", status)
        self.assertTrue("ZeroDivisionError" in exec_result)
        self.assertEqual([], dependencies)
