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
    if (b > a):
        b = 4
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
# grafo.printGrafo()
grafo.geraDot()
