import unittest
from desoper import hello_fisrstpip


class Test_hello(unittest.TestCase):
    def test__working(self):
        self.assertEqual(hello_firstpip.hello(),
                         'Hello, World!', True)


if __name__ == '__main__':
    unittest.main()
