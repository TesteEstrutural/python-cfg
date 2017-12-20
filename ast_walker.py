#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import inspect
from grafo import Grafo
import coverage

class Ast_walker(ast.NodeVisitor):
    def __init__(self, grafo):
        self.grafo = grafo

    def visit_Module(self, node):
        # asts sempre iniciam com módulo,
        #  coloquei ele chamando o resto
        self.generic_visit(node)

    def visit_If(self, node):
        '''Todo If tem os parâmetros test(condição),
        #body(condição satisfeita) e orelse(condição não satisfeita).
        Os nós correspondentes a esses campos ficam dentro deles (são listas).
        *Ajuste para pegar o orelse certo, necessita de mais testes
        '''

        novoNos = []
        #testIf = ((ast.parse(node)))
        #print(dir((testIf).test))
        #todo analizar melhor o parse da ast para o no tentar extrair os dados de condição
        #print(ast.dump((testIf.test)))
        #print(ast.dump((testIf.test.values[1])))
        novoNo = self.grafo.criaNo("If", node.lineno)
        grafo.defCampo("body")
        lastNode = None
        novoNo2 = None
        if not node.body:
            novoNos.append(self.grafo.criaNo("bodyVazio", node.lineno))

        if node.body:
            notTransicao = None
            for no in node.body:
                    print type(no).__name__
                    if type(no).__name__ not in self.grafo.getTipos():
                        notTransicao = no
                        print 'entrei'
                        continue
                    else:
                        if notTransicao != None:
                            self.visit(notTransicao)
                            notTransicao = None
                        lastNode = self.visit(no)
        if notTransicao != None:
            notTransicao = self.visit(notTransicao)
            lastNode = notTransicao
        if(type(lastNode) is list):
            novoNos = lastNode
        else:
            novoNos.append(lastNode)
        grafo.defCampo("orelse")
        if not node.orelse:
            novoNos.append(self.grafo.criaNo("orelseVazioIf", node.lineno))
        if node.orelse:
            #orelse pode ter tamanho maior que 1?
            notTransicao = None
            for no in node.orelse:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if notTransicao != None:
                        self.visit(notTransicao)
                    novoNo2 = self.visit(no)
            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                novoNo2 = notTransicao
            if type(novoNo2) is list:
                while novoNo2:
                    novoNos.append(novoNo2.pop(0))
            else:
                novoNos.append(novoNo2)

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

    def visit_Assign(self, node):
        '''
        '''
        print 'sjueahau'
        print type(node).__name__
        novoNo = self.grafo.criaNo("Assign", node.lineno)
        return novoNo

    def visit_Continue(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Continue", node.lineno)
        novoNo.temFilho = False
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
        novoNo1 = None
        novoNo = self.grafo.criaNo("TryFinally", node.lineno)
        print node.lineno
        grafo.defCampo("body")
        if not node.body:
            self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            for no in node.body:
                novoNo1 = self.visit(no)
        if (type(novoNo1) is list and type(novoNo1[1]) is list):
            novoNo1 = novoNo1[1]
        if not node.finalbody:
            self.grafo.criaNo("bodyVazio", node.lineno)
        finallyNode = None
        if node.finalbody:
            for no in node.finalbody:
                finallyNode = self.grafo.criaNo("Finally", node.lineno)
                self.visit(no)
                finallyNode.setPai(novoNo)
        for no in novoNo1:
            finallyNode.setPai(no)
        return novoNo

    def visit_TryExcept(self, node):
        '''
        '''
        handlerList = []
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
                if (novoNo1 not in n[0].pais):
                    n[0].setPai(novoNo1)
                n.pop(0)
                handlerList.append(n.pop())
        if not node.orelse:
            self.grafo.criaNo("orElseVazioTryExcept", node.lineno)
        if node.orelse:
            for no in node.orelse:
                self.visit(no)
        return [novoNo, handlerList]

    def visit_ExceptHandler(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Except", node.lineno)
        lastNode = None
        print('oi')
        if node.body:
            notTransicao = None
            for no in node.body:
                print type(no).__name__
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if notTransicao != None:
                        self.visit(notTransicao)
                        notTransicao = None
                    lastNode = self.visit(no)
            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                lastNode = notTransicao
        if type(lastNode) is list:
            for no in lastNode:
                no.setSign(1)
        else:
            lastNode.setSign(1)
        if not node.body:
            self.grafo.criaNo("bodyVazio", node.lineno)
        return [novoNo, lastNode]

    def visit_For(self, node):
        '''Visita do for: o último filho do body é pai do for atual,
        orelse suportado, sendo assim, o for atual caso tenha um else associado se torna pai do mesmo
        elses executados apenas se não houver nenhum break no for'''

        novoNo = self.grafo.criaNo("For", node.lineno)
        novoNo1 = None
        iscontinue = False
        lastNode = None
        grafo.defCampo("bodyFor")
        if not node.body:
            novoNo1 = self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            if node.body:
                lastNode = None
                notTransicao = None
                for no in node.body:
                    if type(no).__name__ not in self.grafo.getTipos():
                        notTransicao = no
                        continue
                    else:
                        if notTransicao != None:
                            self.visit(notTransicao)
                            notTransicao = None
                        lastNode = self.visit(no)
                    if type(lastNode) is list:
                        for n in lastNode:
                            if n.getTipo() == "Continue":
                                novoNo.setPai(n)
                        continue
                    if lastNode.getTipo() == "Continue":
                        novoNo.setPai(lastNode)
                if notTransicao != None:
                    notTransicao = self.visit(notTransicao)
                    lastNode = notTransicao
            novoNo1 = lastNode
            if type(novoNo1) is list:
                for n in novoNo1:
                    if n.getTipo() == "Continue":
                        novoNo.setPai(n)
                        continue
                    novoNo.setPai(n)
            else:
                if novoNo1.getTipo() == "Continue":
                    novoNo.setPai(novoNo1)
                else:
                    novoNo.setPai(novoNo1)
        grafo.defCampo("orelseFor")


        if node.orelse:
            if node.orelse:
                i = None
                notTransicao = None
                for no in node.orelse:
                    if type(no).__name__ not in self.grafo.getTipos():
                        notTransicao = no
                        continue
                    else:
                        if notTransicao != None:
                            self.visit(notTransicao)
                            notTransicao = None
                        lastNode = self.visit(no)
                if notTransicao != None:
                    notTransicao = self.visit(notTransicao)
                    lastNode = notTransicao
            novoNo2 = lastNode
            novoNo2.setPai(novoNo)
        grafo.defCampo("fimOrelseFor")
        return novoNo

    def visit_While(self, node):
        '''
        While funciona de maneira idêntica ao for 
        também suportando else
        '''
        novoNo = self.grafo.criaNo("While", node.lineno)
        novoNo1 = None
        iscontinue = False
        lastNode = None
        grafo.defCampo("bodyFor")
        if not node.body:
            novoNo1 = self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            i = None
            notTransicao = None
            for no in node.body:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if notTransicao != None:
                        self.visit(notTransicao)
                    i = self.visit(no)
                if type(i) is list:
                    for n in i:
                        if n.getTipo() == "Continue":
                            novoNo.setPai(n)
                if i.getTipo() == "Continue":
                    novoNo.setPai(i)
            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                lastNode = notTransicao
        novoNo1 = lastNode
        if type(novoNo1) is list:
            for n in novoNo1:
                if n.getTipo() == "Continue":
                    novoNo.setPai(n)
                    continue
                novoNo.setPai(n)
        else:
            if novoNo1.getTipo() == "Continue":
                novoNo.setPai(novoNo1)
            else:
                novoNo.setPai(novoNo1)
        grafo.defCampo("orelseFor")
        novoNo2 = None
        if node.orelse:
            if node.orelse:
                i = None
                notTransicao = None
                for no in node.orelse:
                    if type(no).__name__ not in self.grafo.getTipos():
                        notTransicao = no
                        continue
                    else:
                        if notTransicao != None:
                            self.visit(notTransicao)
                        i = self.visit(no)
                if notTransicao != None:
                    notTransicao = self.visit(notTransicao)
                    lastNode = notTransicao
            novoNo2 = lastNode

            if not node.orelse:
                novoNo2 = self.grafo.criaNo("orelseVazioFor", node.lineno)
            novoNo2.setPai(novoNo)
        grafo.defCampo("fimOrelseFor")
        return novoNo

    def visit_With(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("With", node.lineno)
        if not node.body:
            novoNo1 = self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            i = None
            notTransicao = None
            for no in node.body:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if notTransicao != None:
                        self.visit(notTransicao)
                    i = self.visit(no)
                if type(i) is list:
                    for n in i:
                        if n.getTipo() == "Continue":
                            novoNo.setPai(n)
                if i.getTipo() == "Continue":
                    novoNo.setPai(i)
            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                lastNode = notTransicao
        novoNo1 = lastNode
        if type(novoNo1) is list:
            for n in novoNo1:
                if n.getTipo() == "Continue":
                    novoNo.setPai(n)
                    continue
                novoNo.setPai(n)
        else:
            if novoNo1.getTipo() == "Continue":
                novoNo.setPai(novoNo1)
            else:
                novoNo.setPai(novoNo1)
        grafo.defCampo("orelseFor")
        grafo.defCampo("body")

        return novoNo

    def generic_visit(self, node):
        '''
        Nós de tipos cujas visitas não tiverem sido redefinidas
        pelos métodos acima serão visitadas por esse método.
        '''
        lineno = -1
        #nem todo nó tem o atributo lineno, mas todos os úteis têm
        if hasattr(node, "lineno"):
            lineno = node.lineno
        novoNo = self.grafo.criaNo(type(node).__name__, lineno)
        ast.NodeVisitor.generic_visit(self, node)
        return novoNo

def nq(s):
    b = False
    if True:
        print(12)
        while b:
            if True:
                print(12)
    for b in range(0, 4):
        print(12)

def getCoverage(pythonFile):
    import os
    os.system('coverage annotate ' + pythonFile + '')
    os.system('coverage run ' + pythonFile +'')
    codeAnnotation = []
    with open(pythonFile+',cover','r') as f:
        codeAnnotation = f.readlines()
    codeAnnotation = [(x[1:].strip()).replace('\n', '') for x in codeAnnotation]
    print(codeAnnotation)
    dictResultFile = ast.literal_eval(str(open(".coverage", "r").read()).replace('!coverage.py: This is a private format, don\'t read it directly!', ''))
    os.system('coverage erase ' + pythonFile +'')
    return [dictResultFile['lines'].values()[0], codeAnnotation]
def oi(a):
    for i in a:
        if a:
            a=1
            print(3)
            a=1
        else:
            a = 1
            print('oi')


def shortBubbleSort(alist):
    exchanges = True
    passnum = len(alist)-1
    while passnum > 0 and exchanges:
       exchanges = False
       for i in range(passnum):
           if alist[i]>alist[i+1]:
               exchanges = True
               temp = alist[i]
               alist[i] = alist[i+1]
               alist[i+1] = temp
       passnum = passnum-1
    return alist
def ola(a):
    while a:
        print(4)
        i = 1
def ow(r):
    ''''(x,y) = (5,0)
    try:
      z = x/y
    except ZeroDivisionError:
        pass
    except ZeroDivisionError:
      return 0

    finally:
        print('kk')
    if r:
        pass
    if  r:
        pass
    for i in r:
        print(4)
        if r:
            if r:
                print(r)
                continue
            else:
                print(3)
    print(4)'''
    with r:
        print(4)
        r=5

def shortBubbleSort(alist):
    exchanges = True
    passnum = len(alist)-1
    while passnum > 0 and exchanges:
       exchanges = False
       for i in range(passnum):
           if alist[i]>alist[i+1]:
               exchanges = True
               temp = alist[i]
               alist[i] = alist[i+1]
               alist[i+1] = temp
       passnum = passnum-1
    return alist

grafo = Grafo()
walker = Ast_walker(grafo)
codeAst = ast.parse(inspect.getsource(ow))
#listCoverage = getCoverage('foo2.py')
#print inspect.getsource(shortBubbleSort)
walker.visit(codeAst)
astOfSource = ast.parse(inspect.getsource(shortBubbleSort))
#astOfSource1 = ast.parse(inspect.getsource(o))
#print (ast.dump(astOfSource))
#print ast.dump(astOfSource1)
#grafo.printGrafo()
grafo.geraDot([],[])#listCoverage[0],listCoverage[1])


