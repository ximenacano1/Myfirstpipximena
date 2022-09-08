import unittest
from desoper import hello_firtspip


class Test_hello(unittest.TestCase):
    def test__working(self):
        self.assertEqual(hello_firtspip.hello(),
                         'Hello, World!', True)


if __name__ == '__main__':
    unittest.main()
