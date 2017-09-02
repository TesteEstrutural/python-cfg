#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import inspect
from grafo import Grafo


def foo(a):  # função a ser testada
    a = 3
    b = 4
    if(a<b):
        for i in range(0,5):
            b+=4
            print 'oi'
            if(a<b):
                print 'wab'
            else:
                for k in range(0,4):
                    print 'dub'
                    for o in range(0,3):
                        a = 4
                        c = True
                        while c is True:
                            c = False

    else:
        print 'wauhwuahw'
def oi():
    while True:
        print "vsffffff"
        False

    pass

def iai():
        while True:
            while True:
                print "vsffffff"
                False

def eae():
    l = [3,4,5,6,5]
    o = [['rrrr'],['ll'],['opp']]
    if type(l) is list:
        for i in l:
            print i
            for k in o:
                if (k == 3):
                    print 'll'
                print k
    print 'oi'

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
        novoNos = []

        self.grafo.criaNo("If", node.lineno)
        grafo.defCampo("body")
        if not node.body:
            n = self.grafo.criaNo("bodyVazio", node.lineno)
            novoNos.append(n)
        lastNode = None
        for no in node.body:
            lastNode = self.visit(no)
        novoNos.append(lastNode)
        grafo.defCampo("orelse")
        if not node.orelse:
            lastNode = self.grafo.criaNo("orelseVazio", node.lineno)
            novoNos.append(lastNode)
        for no in node.orelse:
            lastNode = self.visit(no)  # se chamar generic, fura as restrições
        novoNos.append(lastNode)
        grafo.defCampo("fimOrelse")
        return novoNos

    '''def visit_For(self, node):
        novoNo = self.grafo.criaNo("For", node.lineno)
        grafo.defCampo("body")
        if not node.body:
            self.grafo.criaNo("bodyVazio", node.lineno)

        lastNode = None
        if node.body:
            lastNode = node.body.pop()
            print node.body
            for no in node.body:
                self.visit(no)
        lastNode = self.visit(lastNode)
        novoNo.setPai(lastNode)
        grafo.defCampo("orelse")
        if node.orelse:
            print 'HEEEEEEEEEEEY'
            lastNode = node.orelse.pop()
            if grafo.listaNos:
                ola = grafo.listaNos[-1]
                oi = self.visit(node.orelse[0])
                oi.setPai(ola)
                node.orelse.pop(0)
            for no in node.orelse:
                self.visit(no)
        lastNode = self.visit(lastNode)
        novoNo.setPai(lastNode)
        if not node.orelse:
            self.grafo.criaNo("orelseVazio", node.lineno)
        for no in node.orelse:
            self.visit(no)  # se chamar generic, fura as restrições
        grafo.defCampo("fimOrelse")
        return novoNo
'''
    def visit_For(self, node):
        novoNo = self.grafo.criaNo("For", node.lineno)
        novoNo1= None
        novoNo2 = None
        grafo.defCampo("body")
        if not node.body:
            novoNo1 = self.grafo.criaNo("bodyVazio", node.lineno)
        for no in node.body:
            novoNo1 = self.visit(no)
        grafo.defCampo("orelse")
        #if not node.orelse:
           #self.grafo.criaNo("orelseVazio", node.lineno)
        for no in node.orelse:
            novoNo2 = self.visit(no)
            #novoNo2.setPai(novoNo)
        grafo.defCampo("fimOrelse")
        if(type(novoNo1) is list):
            for no in novoNo1:
                novoNo.setPai(no)
        else:
            novoNo.setPai(novoNo1)
        if (type(novoNo2) is list):
            for no in novoNo2:
                novoNo.setPai(no)
        else:
            novoNo.setPai(novoNo2)
        return novoNo

    def visit_While(self, node):
        novoNo = self.grafo.criaNo("While", node.lineno)
        grafo.defCampo("body")
        novoNo1 = None
        if not node.body:
            novoNo1 = self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            for no in node.body:
                novoNo1 = self.visit(no)
        if type(novoNo1) is list:
            for no in novoNo1:
                novoNo.setPai(no)
        else:
            novoNo.setPai(novoNo1)
        return novoNo

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
codeAst = ast.parse(inspect.getsource(foo))
walker.visit(codeAst)
astOfSource = ast.parse(inspect.getsource(foo))
#astOfSource1 = ast.parse(inspect.getsource(o))
print ast.dump(astOfSource)
#print ast.dump(astOfSource1)
#grafo.printGrafo()
grafo.geraDot()
