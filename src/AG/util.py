import random
import numpy as np
from math import ceil


def fixSum(individuo):
    dist = sum(individuo)
    if (dist > 1.0):
        discount = dist - 1.0
        for (index, value) in enumerate(individuo):
            if(value >= discount):
                individuo[index] = value - discount
                break
    elif(dist < 1.0):
        increase = 1.0 - dist
        individuo[random.randrange(len(individuo))] += increase


def geraIndividuo(empresas):
    plen = len(empresas)
    proporcoes = np.zeros(plen)
    while(sum(proporcoes) != 1.0):
        proporcoes[random.randrange(plen)] = random.randrange(100)/100
    return proporcoes


def mutacao(individuo):
    size = len(individuo)
    qtd_mutacoes = random.randrange(ceil(size/3))
    random.seed(random.random())
    for i in range(qtd_mutacoes):
        individuo[random.randrange(size-1)] = random.randrange(100)/100
    fixSum(individuo)


def cruzamento(mae, pai, qtdFIlhos=2):
    random.seed(random.random())
    cortes = [random.randrange(len(mae)-1) for x in range(2)]
    cortes.sort()
    filhos = []
    partesMae = np.array_split(mae, cortes)
    partesPai = np.array_split(pai, cortes)
    filhos.append(np.concatenate(partesMae[0], partesPai[1]))
    filhos.append(np.concatenate(partesPai[0], partesMae[1]))
    for f in filhos:
        fixSum(f)
    return filhos
