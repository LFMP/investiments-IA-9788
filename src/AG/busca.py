import operator
import sys
import os
import numpy as np
if(os.getcwd() not in sys.path):
    sys.path.append(os.getcwd())
from AG.util import cruzamento, geraPopulacao, mutaPopulacao, selecionaPais, weigthEmpresas
from common.read_data import read_data2mov


def buscaGenetica():
    data = read_data2mov()
    empresas = list(data.keys())
    w = weigthEmpresas(data)
    lenIndividuos = len(data)
    populacao = {}
    geraPopulacao(40, lenIndividuos, populacao, w)
    for i in range(50):
        pais = selecionaPais(populacao, 20)
        filhos = cruzamento(pais[0], pais[1], w)
        melhores = []
        for element in sorted(populacao.items(), key=lambda x: x[1], reverse=True)[:10]:
            melhores.append(element[1])
        for f in filhos:
            for m in melhores:
                if(f.ft > m.ft):
                    if (str(m) in populacao):
                        del populacao[str(m)]
                    populacao[str(f)] = f
        mutaPopulacao(populacao, int(len(populacao)/6))
        # print(sorted(populacao.items(),
        #              key=lambda x: x[1], reverse=True)[:1][0][1])
    melhor = sorted(populacao.items(),
                    key=lambda x: x[1], reverse=True)[:1][0][1]
    otimo = {}
    for i in range(lenIndividuos):
        otimo[empresas[i]] = melhor.vetor[i]
    return otimo
