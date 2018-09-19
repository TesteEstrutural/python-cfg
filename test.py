from ast_walker import *
from runner import *
import foo
import unittest
#[insertclass]

funn = foo.shortBubbleSort

elem = dir(foo)
#testSuite = dir(tests.TestMyFunctions())

print(elem)
n_ele = []
for i in elem:
    if callable(getattr(foo,i)):
        n_ele.append(getattr(foo,i))
n_ele = [funn]
inp = [5,6,7]
exp_inp = [5,6]



if __name__ == '__main__':
   print('pdc')
   r = unittest.main(exit=False)
   if r.result.failures:
       failure_str = ""
       for i in r.result.failures[0]:
           failure_str +=str(i)
       test_result = r.result.separator1+"\n "+str(failure_str)+" \n"+r.result.separator2+"\n"
   else:
       test_result = r.result.separator1 + "\n " + "OK, dados fornecidos passaram no teste" + " \n" + r.result.separator2 + "\n"
   for j in n_ele:
        runner(j, "if __name__ == " + "'__main__'" + ":" + "\n\t" + "print (" + j.__name__ + '(' + str(inp) + '))', test_result, j.__name__,inp)
   print(test_result)
