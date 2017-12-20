#!/usr/bin/env python
# -*- coding: utf-8 -*-


class No(object):

    def __init__(self, tipo, numLinha):
        self.tipo = tipo
        self.numLinha = numLinha
        self.pais = []
        self.coberto = False
        self.temFilho = True
        self.sign = 0
        self.filho = []
    def setPai(self, pais):
        if (isinstance(pais, list)):
            while (len(pais) > 0):
                self.pais.append(pais.pop())
        else:
            self.pais.append(pais)

    def setCoberto(self):
        self.coberto = True

    def getTipo(self):
        return self.tipo

    def getNumLinha(self):
        return self.numLinha

    def getPais(self):
        return self.pais

    def getCoberto(self):
        return self.coberto

    def getTipoLinha(self):
        return self.tipo + "\nL: " + str(self.numLinha)

    def setSign(self, sign, no):
        self.sign = sign
        self.filho.append(no)
    def setSign(self, sign):
        self.sign = sign
    def getSign(self):
        return self.sign

    def getFilhos(self):
        return self.filho