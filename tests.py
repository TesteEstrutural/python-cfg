import unittest
import foo
class TestMyFunctions(unittest.TestCase):
    def test_runner(self, fun=foo.shortBubbleSort, inputdado=[3,4,5],outputesperado=[6,3,4,5]):
        self.assertEqual(fun(inputdado), outputesperado)
        self.assertEqual(fun(inputdado), outputesperado)
        self.assertEqual(fun(inputdado), outputesperado)
        self.assertEqual(fun(inputdado), outputesperado)
        print("lancei")
