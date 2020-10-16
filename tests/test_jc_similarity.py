import unittest
from hunahpu.similarity import jc_similarity


class TestJC_similarity(unittest.TestCase):
    def setUp(self):
        self.title1 = "Implementation of industrial technology to improve the manufacturing process contoured seats [Implementación de la tecnología industrial para el mejoramiento del proceso de fabricación de asientos conformados]"
        self.title2 = "Implementation of industrial technology to improve the manufacturing process contoured seats"
        self.title3 = "Implementation of industrial technology to improve the manufacturing process contoured seats"

    def test__working(self):
        self.assertEqual(jc_similarity(self.title2, self.title3), True)

    def test__failing(self):
        self.assertNotEqual(jc_similarity(self.title1, self.title2), False)


if __name__ == '__main__':
    unittest.main()
