import random
import numpy as np
from math import ceil


def desempenho(empresa):
    openValues = empresa[1]
    highValues = empresa[2]
    lowValues = empresa[3]
    closeValues = empresa[4]
    adjCloseValues = empresa[5]
    volumeValues = empresa[6]
    data = [np.array_split(openValues, 7), np.array_split(
        highValues, 7), np.array_split(lowValues, 7), np.array_split(closeValues, 7), np.array_split(adjCloseValues, 7), np.array_split(volumeValues, 7)]
    return np.ceil(np.multiply(np.add(np.subtract(data[3], data[0]), np.subtract(
        data[1], data[2])), np.divide(data[5], np.subtract(data[3], data[4]))))


def weigthEmpresas(empresas):
    weights = []
    for empresa in empresas:
        weights.append(desempenho(empresa))
    return weights


def fitness(individuo, weights):
    fitv = 0
    for (index, value) in enumerate(individuo):
        fitv += np.sum(np.multiply(weights[index], value))
    return fitv/np.sum(individuo)


def fixSum(individuo):
    dist = np.sum(individuo)
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
    while(np.sum(proporcoes) != 1.0):
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
    filhos.append(np.concatenate(partesPai[0], partesMae[1], partesMae[2]))
    filhos.append(np.concatenate(partesMae[0], partesPai[1], partesPai[2]))
    filhos.append(np.concatenate(partesMae[0], partesPai[1], partesMae[2]))
    filhos.append(np.concatenate(partesPai[0], partesMae[1], partesPai[2]))
    filhos.append(np.concatenate(partesMae[0], partesMae[1], partesPai[2]))
    filhos.append(np.concatenate(partesPai[0], partesPai[1], partesMae[2]))
    for f in filhos:
        fixSum(f)
    return filhos
