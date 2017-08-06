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
    pilhaCampo = []  # guarda campos para restaurar (if dentro de if, etc)
    anterior = None
    campo = None  # define se está no body ou orelse de um if, por exemplo
    transicaoDeCampo = False

    def __init__(self):
        pass

    def verificador(self, tipo):
        """
        Verifica se o nó desvia o fluxo.

        Por enquanto, o if que lida com isso de alterar o fluxo só
        verifica se o nó é do tipo If.

        Retorna True caso desvie o fluxo.
        """
        if (self.transicaoDeCampo is True):
            return True  # se tá mudando de campo numa estrutura de controle

        if (self.anterior is None):  # se for o primeiro nó do grafo, o cria
            return True
        if (tipo is not "If" and self.anterior.getTipo() is not "If"):
            return False
        return True

    def defCampo(self, campo):  # define o contexto do próximo nó
        if (campo == "orelse" and self.campo == "body" or
           campo == "fimOrelse" and self.campo == "orelse"):
            self.transicaoDeCampo = True
            self.listaSemFilhos.append(self.anterior)
        self.campo = campo  # pode ser body, orelse, fimOrelse, etc.

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
            if (self.campo == "orelse"):
                no.setPai(self.pilhaIf.pop())
                print "pais: ", no.getPais()

            elif (self.campo == "fimOrelse"):
                lista = []

                # esvazia a lista de nós sem filhos e coloca como pais do nó
                while (len(self.listaSemFilhos) > 0):
                    lista.append(self.listaSemFilhos.pop())
                no.setPai(lista)
        else:
            no.setPai(self.anterior)

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

            self.anterior = no  # nó recém incluido é anterior ao próximo

    def printGrafo(self):
        print "quantidade de nos:", self.numNos
        for no in self.listaNos:
            print no.getTipo(), " filho de: "
            for pai in no.getPais():
                try:
                    print pai.getTipo()
                except (AttributeError):  # se não tiver pais
                    print "Ninguém"

    def printCampo(self):
        print "Campo: ", self.campo

    def geraDot(self):
        dot = Digraph(comment='CFG')
        for no in self.listaNos:
            dot.node(str(no), no.getTipo())
        for no in self.listaNos:
            for pai in no.getPais():
                if (pai is not None):
                    dot.edge(str(pai), str(no))
        print(dot.source)
        dot.render('grafo.gv', view=True)


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
