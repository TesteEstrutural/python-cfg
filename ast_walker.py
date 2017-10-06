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
                return 0
        for k in range(0,4):
            print 'dub'
            for o in range(0,3):
                a = 4
                c = True
                if (a < b):
                    a = b
    else:
        print 'wauhwuahw'
def oi():
    for i in range(0,3):
        if i<3:
            print 3
    else:
        print i
        if (a < b):
            print 'wab'
            if (a < b):
                print 'wab'


def iai():
        while True:
            while True:
                if (a < b):
                    print 'wab'
                    if (a < b):
                        print 'wab'
                while True:
                    print 3



def zap():
    o = True
    if o:
        try:
            a = 10 / 0
        except ZeroDivisionError:
            print("Oops, invalid.")
        except BaseException:
            while a in o:
                print 121
        except BaseException:
            while a in o:
                print 121
        else:
            # Exception didn't occur, we're good.
            pass
        finally:
             return 0

def i():
    i = [1]
    for j in i:
        if True:
            print 9
            break
    pass

class Ast_walker(ast.NodeVisitor):
    def __init__(self, grafo):
        self.grafo = grafo

    def visit_Module(self, node):
        # asts sempre iniciam com módulo, coloquei ele chamando o resto
        self.generic_visit(node)

    def visit_If(self, node):
        '''Todo If tem os parâmetros test(condição),
        #body(condição satisfeita) e orelse(condição não satisfeita).
        Os nós correspondentes a esses campos ficam dentro deles (são listas).
        *Ajuste para pegar o orelse certo, necessita de mais testes
        '''
        novoNos = []
        novoNo = self.grafo.criaNo("If", node.lineno)
        grafo.defCampo("body")
        if not node.body:
            n = self.grafo.criaNo("bodyVazio", node.lineno)
            novoNos.append(n)
        lastNode = None
        if node.body:
            if len(node.body) > 1:
                lastNode = node.body.pop()
                for no in node.body:
                    self.visit(no)
                novoNos.append(self.visit(lastNode))
            else:
                lastNode = node.body.pop()
                novoNos.append(self.visit(lastNode))
        grafo.defCampo("orelse")
        if not node.orelse:
            lastNode = self.grafo.criaNo("orelseVazioIf", node.lineno)
            novoNos.append(lastNode)
        if node.orelse:
            #orelse pode ter tamanho maior que 1?
            '''if len(node.orelse) > 1:

                lastNode = node.orelse.pop()
                for no in node.orelse:
                    self.visit(no)
                novoNos.append(self.visit(lastNode))
            else:
                lastNode = node.orelse.pop()
                novoNos.append(self.visit(lastNode))'''
            visitElse = self.visit(node.orelse[0])
            if type(visitElse) is list:
                visitElse[-1].setPai(novoNo)
            else:
                visitElse.setPai(novoNo)
        grafo.defCampo("fimOrelse")
        #print len(novoNos)
        #novoNos.append(novoNo)
        return novoNos

    def visit_Pass(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Pass", node.lineno)
        novoNo.temFilho = False
        return novoNo

    def visit_Continue(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Continue", node.lineno)
        return novoNo

    def visit_Break(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Break", node.lineno)
        novoNo.temFilho = False
        return novoNo
    def visit_Return(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Return", node.lineno)
        novoNo.temFilho = False
        return novoNo
    def visit_TryFinally(self, node):
        '''
        '''
        #print dir(node)
        #print dir(node.finalbody)
        #print dir(node.body)
        #print 'oi'
        novoNo = self.grafo.criaNo("TryFinally", node.lineno)
        if not node.body:
             self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            for no in node.body:
                self.visit(no)
        if not node.body:
             self.grafo.criaNo("bodyVazio", node.lineno)
        if not node.finalbody:
             self.grafo.criaNo("bodyVazio", node.lineno)
        if node.finalbody:
            for no in node.finalbody:
                n = self.grafo.criaNo("Finally", node.lineno)
                self.visit(no)
                #print dir(n)
                n.setPai(novoNo)
        return novoNo

    def visit_TryExcept(self, node):
        '''
        '''
        print node.orelse
        novoNo = self.grafo.criaNo("TryExcept", node.lineno)
        novoNo1 = None
        if not node.body:
             self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            for no in node.body:
                novoNo1 = self.visit(no)
        if not node.handlers:
            self.grafo.criaNo("handlerVazio", node.lineno)
        if node.handlers:
            for no in node.handlers:
                n = self.visit(no)
                if(novoNo1 not in n.pais):
                    n.setPai(novoNo1)
        if not node.orelse:
            self.grafo.criaNo("orElseVazioTryExcept", node.lineno)
        if node.orelse:
            for no in node.orelse:
                self.visit(no)
        return novoNo

    def visit_ExceptHandler(self, node):

        '''
        '''
        novoNo = self.grafo.criaNo("Except", node.lineno)
        novoNo1 = None
        if node.body:
            novoNo1 = node.body.pop()
            for no in node.body:
                self.visit(no)
            novoNo1 = self.visit(novoNo1)

        if not node.body:
             self.grafo.criaNo("bodyVazio", node.lineno)
        novoNo1.temFilho = False
        return novoNo

    '''def visit_TryFinally(self, node):

        novoNo = self.grafo.criaNo("Finally", node.lineno)
        if node.body:
            for no in node.body:
                self.visit(no)
        if not node.body:
            self.grafo.criaNo("bodyVazio", node.lineno)
        return novoNo'''
    def visit_For(self, node):
        '''
        Visita do for: o último filho do body é pai do for atual, 
        orelse suportado, sendo assim, o for atual caso tenha um else associado se torna pai do mesmo
        elses executados apenas se não houver nenhum break no for
        '''
        novoNo = self.grafo.criaNo("For", node.lineno)
        novoNo1= None
        novoNo2 = None
        grafo.defCampo("body")
        if not node.body:
            novoNo1 = self.grafo.criaNo("bodyVazio", node.lineno)
        else:
            lastNode = node.body.pop()
            for no in node.body:
                self.visit(no)
            novoNo1 = self.visit(lastNode)
        grafo.defCampo("orelse")
        '''Compensa criar orelse vazio sempre? Hummmmmmmm'''
        if node.orelse:
            novoNo2 = self.visit(node.orelse[0])
            for no in node.orelse:
                self.visit(no)
        if not node.orelse:
           novoNo2 = self.grafo.criaNo("orelseVazioFor", node.lineno)
           novoNo2.setPai(novoNo)


        if (type(novoNo2) is list):
            noSonNodes = ["Return", "Pass", "Break"]
            print novoNo2[-1].getTipo()
            #if (novoNo2[-1].getTipo() not in noSonNodes):
                #novoNo2[-1].setPai(novoNo)


        else:
            # print novoNo2.getTipo()
            
            noSonNodes = ["Return", "Pass", "Break"]
            if (novoNo2.getTipo() not in noSonNodes):
                #novoNo2.setPai(novoNo)
                print 'oioioi'

        grafo.defCampo("fimOrelse")
        if(type(novoNo1) is list):
            if(len(novoNo1) >= 3):
                novoNo1.pop()
            for no in novoNo1:
                noSonNodes = ["Return", "Pass", "Break"]
                if no.getTipo() not in noSonNodes:
                   novoNo.setPai(no)

        else:
            noSonNodes = ["Return", "Pass", "Break"]
            if novoNo.getTipo() not in noSonNodes:
                novoNo.setPai(novoNo1)
        return novoNo

    def visit_While(self, node):
        '''
        While funciona de maneira idêntica ao for 
        também suportando else
        '''
        novoNo = self.grafo.criaNo("While", node.lineno)
        grafo.defCampo("body")
        novoNo1 = None
        noElse = None
        print node.orelse
        if not node.body:
            novoNo1 = self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            for no in node.body:
                novoNo1 = self.visit(no)
        if node.orelse:
            novoNo2 = self.visit(node.orelse[0])
            for no in node.orelse:
                self.visit(no)
            if(type(novoNo2) is list):
                novoNo2[-1].setPai(novoNo)
            else:
                novoNo2.setPai(novoNo)

        if type(novoNo1) is list:
            for no in novoNo1:
                novoNo1.pop()
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
codeAst = ast.parse(inspect.getsource(zap))
walker.visit(codeAst)
astOfSource = ast.parse(inspect.getsource(zap))
#astOfSource1 = ast.parse(inspect.getsource(o))
print ast.dump(astOfSource)
#print ast.dump(astOfSource1)
#grafo.printGrafo()
grafo.geraDot()
