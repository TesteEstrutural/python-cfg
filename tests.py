import unittest
import testCoverage
#IMPORT YOUR CODE
import my_func
class TestMyFunctions(unittest.TestCase):
    def test_runner(self):
        self.assertEqual(my_func.shortBubbleSort([1,2,3]), [1,2,3])

    def test_runner2(self):
        self.assertEqual(my_func.shortBubbleSort([3,2,1]), [1, 2, 3])
if __name__ == '__main__':
    unittest.main()