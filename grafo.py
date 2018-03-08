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
    pilhaCampo = [[]]
    fim = False
      # guarda campos para restaurar (if dentro de if, etc)
    anterior = None
    campo = None  # define se está no body ou orelse de um if, por exemplo
    transicaoDeCampo = False
    tiposNo = ["If", "For", "While", "Return", "Continue", "Break", "Pass", "Try", "Except", "Finally", "TryExcept", "With"]
    totNos = 0
    totNosCobertos = 0
    totArestas = 0
    totArestasCobertas = 0
    def __init__(self):
        self.totNos = 0
        self.totNosCobertos = 0
        self.totArestas = 0
        self.totArestasCobertas = 0
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
        '''if (campo == "orelse" and self.campo == "body" or
           campo == "fimOrelse" and self.campo == "orelse" or self.campo == "fimOrelse" and campo == "orelse" or self.campo == "fimOrelse" and campo == "orelse" or
                        campo == "orelseFor" and self.campo == "bodyFor" or
                        campo == "fimOrelseFor" and self.campo == "orelseFor" or self.campo == "fimOrelseFor" and campo == "orelseFor"):
            self.transicaoDeCampo = True
            if((self.anterior).temFilho == True):
                self.listaSemFilhos.append(self.anterior)

        if (campo == "orelseFor" and self.campo == "bodyFor" or
           campo == "fimOrelseFor" and self.campo == "orelseFor" or self.campo == "fimOrelseFor" and campo == "orelseFpr"):
            self.transicaoDeCampo = True
            if((self.anterior).temFilho == True):
                self.listaSemFilhos.append(self.anterior)'''

        self.campo = campo  # pode ser body, orelse, fimOrelse, etc.
        '''if self.pilhaCampo[-1] and len(self.pilhaCampo[-1]) > 2:
            self.pilhaCampo.pop()
            self.fim = True'''
        print('vetorr ' + str(self.pilhaCampo))
        if self.pilhaCampo[-1]:
            eita = []
            for i in self.pilhaCampo[-1]:
                eita.append(i+'For')
            if campo not in self.pilhaCampo[-1] and campo not in eita:
                if (self.pilhaCampo[-1][0] == 'body' and campo =='orelse') or (self.pilhaCampo[-1][0] == 'bodyFor' and campo =='orelseFor'):
                    self.transicaoDeCampo = True
                    print('enrtererere')
                self.pilhaCampo[-1].append(campo)
            else:
                self.pilhaCampo.append([campo])
                self.listaSemFilhos.append(self.anterior)
        else:
            self.pilhaCampo.append([campo])
        for i in range(len(self.pilhaCampo)):
            if len(self.pilhaCampo[i]) == 3:
                print('vetorr del' + str(self.pilhaCampo))
                self.pilhaCampo.pop(i)

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
            print('entrei no if ' + str(self.pilhaCampo))
            print('pilhaIf: '+str(self.pilhaIf))
            print('pilhaFor: ' + str(self.pilhaFor))
            if self.pilhaIf or self.pilhaFor:
                print('entrei aqwu')
                print('pilhaFor: ' + str(self.pilhaIf))


                no.setPai(self.pilhaIf.pop())

                print('pilhaIf: ' + str(self.pilhaIf))
                lista = []
                self.fim = False
                print('vlws ' + str(self.pilhaCampo))

                print('vlws dps ' + str(self.pilhaCampo))
                # esvazia a lista de nós sem filhos e coloca como pais do nó
                print('list s filh'+str(self.listaSemFilhos))
                while (len(self.listaSemFilhos) > 0):
                    o = self.listaSemFilhos.pop()
                    print('mercy sucks')
                    if o.temFilho == True:
                        lista.append(o)
                    if no.getTipo() == "Except":
                        for i in range(len(lista)):
                            if lista[i].getSign() == True:
                                no.setPai(lista[i])
                        continue
                    else:
                        no.setPai(lista)
            '''if (self.campo == "fimOrelse" or self.campo ==  "fimOrelseFor"):
                lista = []
                for i in range(0,2):
                    self.pilhaCampo.pop()
'''

                #self.campo = self.pilhaCampo[-1]
            #if self.fim:#self.pilhaCampo[-2][-1] =='fimOrelse':

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
                    print (pai.getTipo())
                except (AttributeError):  # se não tiver pais
                    print ("Ninguém")

    def printCampo(self):
        print "Campo: ", self.campo

    def geraDot(self, listCoverage, listSource, sourceCode):
        dot = Digraph(comment='CFG')
        for i in self.listaNos:
            if i.getSign():
                print('euuu ' +str(i.getTipo()))
        for no in self.listaNos:
            if no.getPais() and no.getTipo() == "Except":
                print('entrei')
                for i in no.getPais():
                    if i is not None and i.getSign() != True:
                            no.getPais().remove(i)

        '''for no in self.listaNos:
            pais = []
            if no.getPais():
                for i in no.getPais():
                    if i is not None and i.getSignInvalido() and no.getTipo()!= "For" and no.getTipo()!= "While" and no.getTipo()!= "Finally" and no.getTipo()!= "Except"  and (i.getNumLinha()<no.getNumLinha()):
                        no.setSignInvalido(True)
                        break'''
        '''
        for no in self.listaNos:
            if no.getSignInvalido():
                print('genji')'''

        for no in self.listaNos:
            if no.getNumLinha() in listCoverage and listSource:
                if no.getTipo() == "Return" or no.getTipo() == "Break" or no.getTipo() == "Pass":
                    dot.node(str(no), no.getTipoLinha()+'\n'+listSource[no.getNumLinha() - 1], color='green', style="bold")
                    self.totNos +=1
                    self.totNosCobertos += 1
                    continue
                else:
                    dot.node(str(no), no.getTipoLinha()+'\n'+listSource[no.getNumLinha() - 1], color='green')
                    self.totNos += 1
                    self.totNosCobertos += 1
                    continue
            if listSource:
                if no.getSignInvalido():
                    dot.node(str(no), no.getTipoLinha()+'\n'+listSource[no.getNumLinha() - 1], color='red')
                else:
                    dot.node(str(no), no.getTipoLinha() + '\n' + listSource[no.getNumLinha() - 1])
                self.totNos += 1
            else:
                if (no.getTipo() == "Return" or no.getTipo() == "Break" or no.getTipo() == "Pass") and no.getSignInvalido():
                    dot.node(str(no), no.getTipoLinha() + '\n', style="bold", color="red")
                    self.totNos += 1
                    continue
                if no.getTipo() == "Return" or no.getTipo() == "Break" or no.getTipo() == "Pass":
                    dot.node(str(no), no.getTipoLinha() + '\n', style="bold")
                    self.totNos += 1
                    continue
                if no.signInvalido():
                    dot.node(str(no), no.getTipoLinha() + '\n', color="red", style="bold")
                    self.totNos += 1
                    continue
                else:
                    dot.node(str(no), no.getTipoLinha() + '\n')
                    self.totNos += 1

        for no in self.listaNos:
            pais = []

            if no.getPais():

                '''for i in no.getPais():
                    if i is not None and i.getSignInvalido() and (no.getTipo()!= "Finally" or no.getTipo()!= "Except"):
                        no.setSignInvalido(True)
                        print('oioioioioisssss')'''

                '''for i in no.getPais():
                    if (i is not None) and (i.getSign() != True) and (no.getTipo()== "Except"):
                        no.getPais().remove(i)'''

                pais = list(set(no.getPais()))
                po = len(pais)-1
                i = 0

                while i <= po:
                    if hasattr(pais[i], 'getTipo'):
                        if (pais[i].getTipo() == "Break" or pais[i].getTipo() == "Pass" or pais[i].getTipo() == "Return") and no.getTipo() != "Finally" and not no.getSignInvalido():
                            pais.pop(i)
                            po = len(pais)-1
                            continue
                    i+=1

                for pai in pais:
                    if (pai is not None):
                        if no.getNumLinha() in listCoverage and pai.getNumLinha() in listCoverage and no.getTipo() == "Except" and pai.getSign() == True:
                            dot.edge(str(pai), str(no), style='dashed', color='green')
                            self.totArestasCobertas+=1
                            self.totArestas+=1
                            continue


                        if no.getNumLinha() in listCoverage and pai.getNumLinha() in listCoverage:
                            dot.edge(str(pai), str(no), color='green')
                            self.totArestasCobertas += 1
                            self.totArestas += 1
                            continue
                        if no.getTipo() == "Except" and pai.getSign() == True:
                            dot.edge(str(pai), str(no), style ='dashed')
                            self.totArestas += 1
                            continue
                        if no.getSignInvalido() or pai.getSignInvalido():
                            dot.edge(str(pai), str(no), style='dotted', color = "red")
                            continue

                        else:
                            dot.edge(str(pai), str(no))
                            self.totArestas += 1

        '''dot.node('nos: '+str(self.totNos))
        dot.node('coberto: '+ str(self.totNosCobertos))
        dot.node("arestas: \n"+str(self.totArestas))
        dot.node("arestas cobertas : \n" + str(self.totArestasCobertas))'''
        dot.node("Cobertura por nos: \n " + str(round((float(self.totNosCobertos) / float(self.totNos)), 3)),
                 shape='box')
        dot.node("Cobertura por arestas: \n " + str(round((float(self.totArestasCobertas) / float(self.totArestas)), 3)),
                 shape='box')
        dot.node("Source code: \n\t"+ sourceCode, shape='box'  )
        dot.render('grafo.gv', view=True, )
