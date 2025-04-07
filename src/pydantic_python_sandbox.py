import asyncio

from tools import execute_code

CODE = """
import numpy
a = numpy.array([1, 2, 3])
print(a)
a
"""


if __name__ == '__main__':
    asyncio.run(execute_code(code=CODE,debug=True))
