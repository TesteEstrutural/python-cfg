#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import inspect
from grafo import Grafo


def foo(a):  # função a ser testada
    b = 2 + a
    if (b > 2):
        print a
        print b
        if (a > b):
            print 3
            if(a == 4):
                print "asd"
    else:
        print a
        print "asfsad"
        a = 123
        b = 234
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
        os nós correspondentes a esses campos ficam dentro deles
        '''
        self.grafo.criaNo("If", 0)
        print "\nIF: BLOCOS:"
        print "test: ", node.test
        # self.generic_visit(node.test)
        print "body: ", node.body
        grafo.defCampo("body")
        if (len(node.body) == 0):
            self.grafo.criaNo("bodyVazio", 0)
        for no in node.body:
            self.visit(no)
        print "orelse: ", node.orelse, "\n"
        grafo.defCampo("orelse")
        if (len(node.orelse) == 0):
            self.grafo.criaNo("orelseVazio", 0)
        for no in node.orelse:
            self.visit(no)  # se chamar generic, fura as restrições
        # o foco está sendo aqui
        grafo.defCampo("fimOrelse")

    def generic_visit(self, node):
        '''
        Nós de tipos cujas visitas não tiverem sido redefinidas
        pelos métodos acima serão visitadas por esse método.
        '''
        print type(node).__name__
        self.grafo.criaNo(type(node).__name__, 0)
        ast.NodeVisitor.generic_visit(self, node)


grafo = Grafo()
walker = Ast_walker(grafo)
codeAst = ast.parse(inspect.getsource(foo))
walker.visit(codeAst)
grafo.printGrafo()
grafo.geraDot()
