#!/usr/bin/env python
# -*- coding: utf-8 -*-


class No(object):
    tipo = None
    numLinha = None
    pais = []
    coberto = False

    def __init__(self, tipo, numLinha):
        self.tipo = tipo
        self.numLinha = numLinha

    def setPai(self, pai):
        self.pais.append(pai)

    def setCoberto(self):
        self.coberto = True
