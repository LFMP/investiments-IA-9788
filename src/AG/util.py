import random
import numpy as np
from math import ceil


class Individuo:
    def __init__(self, vetor, ft=0):
        self.vetor = vetor
        self.ft = ft

    def fitness(self, weights):
        for (index, value) in enumerate(self.vetor):
            self.ft += np.sum(np.multiply(weights[index], value))
        self.ft = self.ft/np.sum(self.vetor)


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


def fixSum(individuo):
    dist = np.sum(individuo.vetor)
    if (dist > 1.0):
        discount = dist - 1.0
        for (index, value) in enumerate(individuo.vetor):
            if(value >= discount):
                individuo.vetor[index] = value - discount
                break
    elif(dist < 1.0):
        increase = 1.0 - dist
        individuo.vetor[random.randrange(len(individuo))] += increase


def geraIndividuo(qtdElementos, w):
    proporcoes = np.zeros(qtdElementos)
    while(np.sum(proporcoes) != 1.0):
        proporcoes[random.randrange(qtdElementos)] = random.randrange(100)/100
    ind = Individuo(proporcoes)
    ind.fitness(w)
    return ind


def geraPopulacao(qtdIndividuos, qtdElementos, populacao, w):
    for i in range(qtdIndividuos):
        individuo = geraIndividuo(qtdElementos, w)
        populacao[str(individuo)] = individuo


def mutacao(individuo):
    size = len(individuo.vetor)
    qtd_mutacoes = random.randrange(ceil(size/3))
    random.seed(random.random())
    for i in range(qtd_mutacoes):
        individuo.vetor[random.randrange(size-1)] = random.randrange(100)/100
    fixSum(individuo)


def cruzamento(mae, pai, w, qtdFIlhos=6):
    random.seed(random.random())
    cortes = [random.randrange(len(mae)-1) for x in range(2)]
    cortes.sort()
    filhos = []
    partesMae = np.array_split(mae.vetor, cortes)
    partesPai = np.array_split(pai.vetor, cortes)
    filhos.append(Individuo(np.concatenate(
        partesPai[0], partesMae[1], partesMae[2])))
    filhos.append(Individuo(np.concatenate(
        partesMae[0], partesPai[1], partesPai[2])))
    filhos.append(Individuo(np.concatenate(
        partesMae[0], partesPai[1], partesMae[2])))
    filhos.append(Individuo(np.concatenate(
        partesPai[0], partesMae[1], partesPai[2])))
    filhos.append(Individuo(np.concatenate(
        partesMae[0], partesMae[1], partesPai[2])))
    filhos.append(Individuo(np.concatenate(
        partesPai[0], partesPai[1], partesMae[2])))
    for i in range(qtdFIlhos):
        fixSum(filhos[i])
        filhos[i].fitness(w)
    return filhos
