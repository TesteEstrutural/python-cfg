import unittest
import testCoverage
class TestMyFunctions(unittest.TestCase):
    def test_runner(self, fun=testCoverage.shortBubbleSort, inputdado=[3,4,5],outputesperado=[6,3,4,5]):
        self.assertEqual(fun(inputdado), outputesperado)
    def test_runner2(self, fun=testCoverage.shortBubbleSort, inputdado=[3,4,5],outputesperado=[6,3,4,5]):
        self.assertEqual(fun([4,1,6]), outputesperado)
