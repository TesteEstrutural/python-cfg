#!/usr/bin/env python
# -*- coding: utf-8 -*-
from No import No


class Grafo:
    """Gera um grafo cujos nós vão sendo
    definidos a partir de seu tipo, número de linha,
    etc.
    para gerar o .dot, faz-se uma busca em profundidade
    reversa (tem nome pra isso?) partindo dos nós sem filhos
    ou de nós de retorno e percorrendo por seus pais.

    """

    numNos = 0
    listaNos = []
    listaSemFilhos = []  # para usar como pais do nó seguinte ao orelse
    listaReturn = []
    pilhaIf = []
    anterior = None
    campo = None  # define se está no body ou orelse de um if

    def __init__(self):
        pass

    def criaAresta(self):
        pass

    def verificador(self, tipo):
        """
        Verifica se o nó desvia o fluxo.

        Por enquanto, o if que lida com isso de alterar o fluxo só
        verifica se o nó é do tipo If.

        Retorna True caso desvie o fluxo
        """

        if (self.anterior is None):
            return True
        if (tipo is not "If" and self.anterior is not "If"):
            return False
        return True

    def defCampo(self, campo):  # define se o próximo está em um body ou orelse
        self.campo = campo

    def criaNo(self, tipo, numlinha):
        """
        Cria nó apenas se ele mudar o fluxo do programa, para que
        não se repitam nós seguidos que não alterem o fluxo;
        para duas atribuições seguidas, por exemplo, será criado
        apenas um nó.
        """

        if (not self.verificador(tipo)):
            pass  # se não altera fluxo, ignora o nó da ast e não cria no grafo
        else:
            self.numNos += 1
            no = No(self, tipo, numlinha)
            self.listaNos.append(no)
            if (tipo == "If"):
                self.pilhaIf.append(no)

            # Quando for o primeiro elemento do orelse, define o pai dele
            # como o if mais recente da pilha e desempilha esse if.
            if (self.campo == "orelse"):
                no.setPai(self.pilhaIf.pop())
                self.defCampo(None)
            no.setPai(self.anterior)
