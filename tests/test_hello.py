import unittest
from hello import hello
class Test_hello(unittest.TestCase):
    def test__working(self):
        self.assertEqual( hello(),
                          'Hello, World!' , True)

if __name__ == '__main__':
    unittest.main()
