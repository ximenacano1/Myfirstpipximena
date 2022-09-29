import unittest
from AnomaliesXimena import Anomalies


class Test_Anomalies(unittest.TestCase):
    def test__working(self):
        self.assertEqual(len(Anomalies.quiral_solutions(5)), 11, True)
        # self.assertEqual(len(Anomalies.quiral_solutions(6)), 112, True)


if __name__ == '__main__':
    unittest.main()
