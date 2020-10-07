import operator
import sys
import os
import numpy as np
if(os.getcwd() not in sys.path):
    sys.path.append(os.getcwd())
from src.AG.util import cruzamento, geraPopulacao, mutaPopulacao, selecionaPais, weigthEmpresas
from src.common.read_data import read_data2mov


def buscaGenetica():
    data = read_data2mov()
    empresas = list(data.keys())
    w = weigthEmpresas(data)
    lenIndividuos = len(data)
    populacao = {}
    geraPopulacao(2000, lenIndividuos, populacao, w)
    for i in range(1000):
        pais = selecionaPais(populacao, 20)
        filhos = cruzamento(pais[0], pais[1], w)
        inseridos = 0
        for f in filhos:
            if str(f) not in populacao:
                inseridos += 1
                populacao[str(f)] = f
        if inseridos > 0:
            piores = []
            for element in sorted(populacao.items(), key=lambda x: x[1], reverse=False)[:inseridos]:
                piores.append(element[1])
            for p in range(len(piores)):
                del populacao[str(piores[p])]
        mutaPopulacao(populacao, int(len(populacao)/6))
        # print(sorted(populacao.items(),
        #              key=lambda x: x[1], reverse=True)[:1][0][1])
    melhor = sorted(populacao.items(),
                    key=lambda x: x[1], reverse=True)[:1][0][1]
    otimo = {}
    for i in range(lenIndividuos):
        otimo[empresas[i]] = melhor.vetor[i]
    return otimo


# print(buscaGenetica())
