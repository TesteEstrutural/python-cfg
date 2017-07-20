#!/usr/bin/env python
# -*- coding: utf-8 -*-
import No


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
    listaSemFilhos = []
    listaReturn = []
    pilhaIf = []
    anterior = None

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

            no.setPai()
