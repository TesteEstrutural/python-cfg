from ast_walker import *
import unittest
from foo import *
class TestMyFunctions(unittest.TestCase):
    def test_shortBubbleSort(self,func=oii,inputdado=0,outputesperado=0):
        runner(func, "if __name__ == "+"'__main__'"+":"+"\n\t"+"print ("+func.__name__+'('+str(inputdado)+'))')
        print(func.__name__)
        "if __name__ == ""__main__"":"+"\n\t"+"print ("+func.__name__+'('+str(inputdado)+'))'
        self.assertEqual(func(inputdado), outputesperado)


if __name__ == '__main__':
    unittest.main(exit=False)