import random
import numpy as np
from random import randrange


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


def cruzamento(mae, pai, qtdFIlhos=1):
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
