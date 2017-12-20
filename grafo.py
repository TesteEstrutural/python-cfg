#!/usr/bin/env python
# -*- coding: utf-8 -*-
from no import No
from graphviz import Digraph


class Grafo:
    """Gera um grafo cujos nós vão sendo
    definidos a partir de seu tipo, número de linha,
    etc.

    Disponibiliza a opção de gerar uma visualização do grafo
    utilizando a ferramenta graphviz.
    """

    numNos = 0
    listaNos = []
    listaSemFilhos = []  # para usar como pais do nó seguinte ao orelse
    listaReturn = []
    pilhaIf = []
    pilhaFor = []
    pilhaWhile = []
    pilhaCampo = []  # guarda campos para restaurar (if dentro de if, etc)
    anterior = None
    campo = None  # define se está no body ou orelse de um if, por exemplo
    transicaoDeCampo = False
    tiposNo = ["If", "For", "While", "Return", "Continue", "Break", "Pass", "Try", "Except", "Finally", "TryExcept", "With"]

    def __init__(self):
        pass

    def verificador(self, tipo):
        """
        Verifica se o nó desvia o fluxo.
        Por enquanto, o if que lida com isso de alterar o fluxo só
        verifica se o nó é do tipo If.
        Retorna True caso desvie o fluxo."""

        if (self.transicaoDeCampo is True):
            return True  # se tá mudando de campo numa estrutura de controle
        if (tipo == "Module"):
            return False
        if (self.anterior is None):  # se for o primeiro nó do grafo, o cria
            return True
        if tipo not in self.tiposNo and self.anterior.getTipo() not in self.tiposNo:
            return False
        return True

    def defCampo(self, campo):  # define o contexto do próximo nó
        if (campo == "orelse" and self.campo == "body" or
           campo == "fimOrelse" and self.campo == "orelse"):
            self.transicaoDeCampo = True
            if((self.anterior).temFilho == True):
                self.listaSemFilhos.append(self.anterior)
        if (campo == "orelseFor" and self.campo == "bodyFor" or
           campo == "fimOrelseFor" and self.campo == "orelseFor"):
            self.transicaoDeCampo = True
            if((self.anterior).temFilho == True):
                self.listaSemFilhos.append(self.anterior)
        self.campo = campo  # pode ser body, orelse, fimOrelse, etc.
        self.pilhaCampo.append(campo)

    def defPai(self, no):
        """
        Quando for o primeiro elemento do orelse, define o pai dele
        como o if mais recente da pilha e desempilha esse if.

        Quando for o primeiro elemento depois de um orelse, define
        seus pais como sendo todos os nós sem filhos (que não são return).

        Caso contrário, define o pai como sendo o nó anterior.
        """
        if (self.transicaoDeCampo is True):
            self.transicaoDeCampo = False
            if self.campo == "orelse" and self.pilhaIf:
                no.setPai(self.pilhaIf.pop())
            if (self.campo == "fimOrelse" or self.campo ==  "fimOrelseFor" or self.campo ==  "fimOrelseWhile"):
                lista = []
                for i in range(0,2):
                    self.pilhaCampo.pop()

                self.campo = self.pilhaCampo[-1]

                # esvazia a lista de nós sem filhos e coloca como pais do nó
                while (len(self.listaSemFilhos) > 0):
                    o = self.listaSemFilhos.pop()
                    if o.temFilho == True :
                        lista.append(o)
                    no.setPai(lista)

        else:
            no.setPai(self.anterior)
    def getTipos(self):
        return self.tiposNo

    def criaNo(self, tipo, numlinha):
        """
        Cria nó apenas se ele mudar o fluxo do programa, para que
        não se repitam nós seguidos que não alterem o fluxo;
        para duas atribuições seguidas, por exemplo, será criado
        apenas um nó.
        """

        if (not self.verificador(tipo)):
            pass  # se não altera fluxo, ignora nó da ast e não cria no grafo
        else:
            no = No(tipo, numlinha)
            self.defPai(no)
            self.numNos += 1
            self.listaNos.append(no)
            if (tipo == "If"):
                self.pilhaIf.append(no)
            if (tipo == "Return"):
                self.listaReturn.append(no)
            # Definir os outros tipos aqui.
            if (tipo == "For"):
                self.pilhaFor.append(no)
            if (tipo == "While"):
                self.pilhaWhile.append(no)

            self.anterior = no # nó recém incluido é anterior ao próximo
            return self.anterior

    def printGrafo(self):
        #print "quantidade de nos: ", self.numNos
        for no in self.listaNos:
            #print no.getTipo(), "numLinha: ", no.getNumLinha(), " filho de:"
            for pai in no.getPais():
                try:
                    print pai.getTipo()
                except (AttributeError):  # se não tiver pais
                    print "Ninguém"

    def printCampo(self):
        print "Campo: ", self.campo

    def geraDot(self, listCoverage, listSource):
        dot = Digraph(comment='CFG')
        #assigns = {'getNo': None, 'getTipo':'Assign', 'getLinha':''}
        #assignsList = []
        #lastAssign = None
        for no in self.listaNos:

            '''if no.getTipo() =='Assign':
                assigns['getLinha'] +=str(no.getNumLinha())+' '
                assigns['getNo'] = no
                assignsList.append(no)
                continue
            else:
                if assigns['getNo'] != None:
                    dot.node(str(assigns['getNo']), assigns['getTipo']+'\nL: '+assigns['getLinha'])
                assigns['getNo'] = None
                assigns['getLinha'] = ''
                if assignsList:
                    lastAssign = assignsList.pop()'''
            if no.getNumLinha() in listCoverage:
                dot.node(str(no), no.getTipoLinha(), color='green')
            if listSource:
                dot.node(str(no), no.getTipoLinha()+'\n'+listSource[no.getNumLinha() - 1])
            else:
                dot.node(str(no), no.getTipoLinha() + '\n')
        for no in self.listaNos:
            if no.getPais():
                pais = list(set(no.getPais()))
                p = len(pais) - 1
                filter(lambda p : hasattr(p, 'getTipo') and (p.getTipo() == "Continue" or p.getTipo() == "Return" or p.getTipo() == "Pass" or p.getTipo() == "Break") and no.getTipo() != "Finally", pais)


                p = len(pais) - 1
                if no.getTipo() == "Except":
                    for i in range(0, p):
                        if pais[i].getSign() == 1:
                            pais.pop(i)
                for pai in pais:
                    if (pai is not None):
                        if no.getNumLinha() in listCoverage and pai.getNumLinha() in listCoverage and no.getTipo() == "Except":
                            dot.edge(str(pai), str(no), style='dashed', color='green')
                            continue
                        if no.getNumLinha() in listCoverage and pai.getNumLinha() in listCoverage:
                            dot.edge(str(pai), str(no), color='green')
                            continue
                        if no.getTipo() == "Except" and no.getSign !=1:
                            dot.edge(str(pai), str(no), style ='dashed')
                            continue

                        else:
                            dot.edge(str(pai), str(no))
        dot.render('grafo.gv', view=True)
'''
grafo = Grafo()
grafo.criaNo("assignment", 0)
grafo.criaNo("If", 0)
grafo.defCampo("body")
grafo.criaNo("assignment", 3)
grafo.criaNo("assignment", 3)
grafo.defCampo("orelse")
grafo.criaNo("assignment", 3)
grafo.criaNo("assignment", 3)
grafo.defCampo("fimOrelse")
grafo.criaNo("assignment", 3)
grafo.criaNo("assignment", 3)
grafo.criaNo("If", 5)
print "printando grafo"
grafo.printGrafo()

grafo.geraDot()
'''
