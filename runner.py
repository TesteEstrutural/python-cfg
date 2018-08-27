import ast
import inspect
from geraDot import *
import coverage
from grafo import Grafo
from ast_walker import *
from instrumentation import *
import sys

def runner(nomeFunc, mainString, testResult, fun_name):
    grafo = Grafo()
    walker = Ast_walker(grafo)
    codeAst = ast.parse(inspect.getsource(nomeFunc))
    listCoverage = getCoverage(nomeFunc, mainString)
    print(inspect.getsource(nomeFunc))
    # print inspect.getsource(shortBubbleSort)
    walker.visit(codeAst)
    # astOfSource1 = ast.parse(inspect.getsource(o))
    # print (ast.dump(astOfSource))
    # print ast.dump(astOfSource1)
    # grafo.printGrafo()
    print "aa"+ str(listCoverage[1])
    geraDot(grafo.listaNos,listCoverage[0],listCoverage[1],listCoverage[2], testResult, fun_name)
    del grafo