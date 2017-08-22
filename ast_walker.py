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
    for i in range(0, 5):
        print "aaa"
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
    while True:
        print "vsffffff"
        False
    pass

def iai():
    a = 98
    if a <98:
        print 'oi'
        if a>98:
            print 'mds'


def eae():
    i=0
    while i<4:
        print i
        j=0
        i+=1
        while j<8:
            print j
            k=0
            j += 1
            for k in range(0, 8):
                print k
                k += 1
                for k in range(0, 8):
                    print k
                    k += 1


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
        if not node.body:
            self.grafo.criaNo("bodyVazio", node.lineno)
        for no in node.body:
            self.visit(no)
        grafo.defCampo("orelse")
        if not node.orelse:
            self.grafo.criaNo("orelseVazio", node.lineno)
        for no in node.orelse:
            self.visit(no)  # se chamar generic, fura as restrições

        grafo.defCampo("fimOrelse")


    def visit_For(self, node):
        novoNo = self.grafo.criaNo("For", node.lineno)
        ultimoBody = None
        grafo.defCampo("body")
        #ultimoFor = grafo.pilhaFor

        if not node.body:
            self.grafo.criaNo("bodyVazio", node.lineno)
        for no in node.body:
            ultimoBody = self.visit(no)
            novoNo.setPai(ultimoBody)
        grafo.defCampo("orelse")
        if not node.orelse:
            self.grafo.criaNo("orelseVazio", node.lineno)
        for no in node.orelse:
            self.visit(no)  # se chamar generic, fura as restrições
        grafo.defCampo("fimOrelse")
        i=0
        while grafo.pilhaFor and i < 1:
            grafo.pilhaFor[-1].setPai(novoNo)
            i=1
        while grafo.pilhaWhile and i < 1:
            grafo.pilhaWhile[-1].setPai(novoNo)
            i=1



    def visit_While(self, node):
        novoNo = self.grafo.criaNo("While", node.lineno)
        novoNo1 = None
        grafo.defCampo("body")
        if not node.body:
            self.grafo.criaNo("bodyVazio", node.lineno)
        for no in node.body:
            novoNo1 = self.visit(no)
            novoNo.setPai(novoNo1)
        grafo.defCampo("fimOrelse")
        i = 0
        while grafo.pilhaWhile and i < 1:
            grafo.pilhaWhile[-1].setPai(novoNo)
            i = 1

    '''def visit_Print(self, node):
        novoNo = self.grafo.criaNo("Print", node.lineno)
        grafo.defCampo("body")
        if novoNo.pais:
            for pais in novoNo.pais:
                if(pais.getTipo() is "For" or "While"):
                    pais.setPai(novoNo)
'''






    def generic_visit(self, node):
        '''
        Nós de tipos cujas visitas não tiverem sido redefinidas
        pelos métodos acima serão visitadas por esse método.
        '''
        lineno = -1
        novoNo = None
        # nem todo nó tem o atributo lineno, mas todos os úteis têm
        if hasattr(node, "lineno"):
            lineno = node.lineno
        novoNo = self.grafo.criaNo(type(node).__name__, lineno)
        ast.NodeVisitor.generic_visit(self, node)
        return novoNo

grafo = Grafo()
walker = Ast_walker(grafo)
codeAst = ast.parse(inspect.getsource(eae))
walker.visit(codeAst)
astOfSource = ast.parse(inspect.getsource(eae))
#astOfSource1 = ast.parse(inspect.getsource(o))
print ast.dump(astOfSource)
#print ast.dump(astOfSource1)
grafo.printGrafo()
grafo.geraDot()
