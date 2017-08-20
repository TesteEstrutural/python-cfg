#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import inspect
from grafo import Grafo


def foo(a):  # função a ser testada
    b = 2 + a
    for i in range(0, 5):
        print b
    if (b > 2):
        print a
        print b
        if (a > b):
            print 3
            if(a == 4):
                while i in range(0,4):
                    print "asd"
    for i in range(0, 5):
        for o in range(0, 5):
            print b
    else:
        print a
        print "asfsad"
        a = 123
        b = 234
    if (b > a):
        b = 4
        pass
def oi():
    for x in range(0,1):
        print "vsffffff"
    pass



def ola():
    i =9
    if(i<3):
        print i
    else:
        print 'ooo'
def o():
    print 'oo'
    pass

class Ast_walker(ast.NodeVisitor):

    def __init__(self, grafo):
        self.grafo = grafo

    def visit_Module(self, node):
        # asts sempre iniciam com módulo, coloquei ele chamando o resto
        self.generic_visit(node)

    def visit_If(self, node):
        '''Todo If tem os parâmetros test(condição),
        body(condição satisfeita) e orelse(condição não satisfeita).
        Os nós correspondentes a esses campos ficam dentro deles (são listas).
        '''
        self.grafo.criaNo("If", node.lineno)
        grafo.defCampo("body")
        if (len(node.body) == 0):
            self.grafo.criaNo("bodyVazio", node.lineno)
        for no in node.body:
            self.visit(no)
        grafo.defCampo("orelse")
        if (len(node.orelse) == 0):
            self.grafo.criaNo("orelseVazio", node.lineno)
        for no in node.orelse:
            self.visit(no)  # se chamar generic, fura as restrições

        grafo.defCampo("fimOrelse")


    def visit_For(self, node):
        novoNo = self.grafo.criaNo("For", node.lineno)
        grafo.defCampo("body")
        if (len(node.body) == 0):
            self.grafo.criaNo("bodyVazio", node.lineno)
        for no in node.body:
            self.visit(no)
        grafo.defCampo("orelse")
        if (len(node.orelse) == 0):
            self.grafo.criaNo("orelseVazio", node.lineno)

        for no in node.orelse:
            self.visit(no)  # se chamar generic, fura as restrições
        if grafo.anterior.getTipo() is "For":
            novoNo.setPai(grafo.anterior)
            grafo.pilhaFor.pop()
            print "ioioio"
        grafo.defCampo("fimOrelse")

    def visit_While(self, node):
        novoNo = self.grafo.criaNo("While", node.lineno)
        grafo.defCampo("body")
        if (len(node.body) == 0):
            self.grafo.criaNo("bodyVazio", node.lineno)
        for no in node.body:
            self.visit(no)
        grafo.defCampo("orelse")
        if (len(node.orelse) == 0):
            self.grafo.criaNo("orelseVazio", node.lineno)

        for no in node.orelse:
            self.visit(no)  # se chamar generic, fura as restrições
        if grafo.anterior.getTipo() is "For":
            novoNo.setPai(grafo.anterior)
            grafo.pilhaFor.pop()
            print "ioioio"
        grafo.defCampo("fimOrelse")

    def visit_Print(self, node):
        novoNo = self.grafo.criaNo("Print", node.lineno)
        grafo.defCampo("body")





    def generic_visit(self, node):
        '''
        Nós de tipos cujas visitas não tiverem sido redefinidas
        pelos métodos acima serão visitadas por esse método.
        '''
        lineno = -1
        # nem todo nó tem o atributo lineno, mas todos os úteis têm
        if hasattr(node, "lineno"):
            lineno = node.lineno
        self.grafo.criaNo(type(node).__name__, lineno)
        ast.NodeVisitor.generic_visit(self, node)


grafo = Grafo()
walker = Ast_walker(grafo)
codeAst = ast.parse(inspect.getsource(foo))
walker.visit(codeAst)
#astOfSource = ast.parse(inspect.getsource(oi))
#astOfSource1 = ast.parse(inspect.getsource(o))
#print ast.dump(astOfSource)
#print ast.dump(astOfSource1)
grafo.printGrafo()
grafo.geraDot()
