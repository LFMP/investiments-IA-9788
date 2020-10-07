import random
import numpy as np
import copy
from math import ceil

from numpy.core.defchararray import count


class Individuo:
    def __init__(self, vetor, ft=0):
        self.vetor = vetor
        self.ft = ft

    def __lt__(self, other): return self.ft > other.ft
    def __gt__(self, other): return self.ft < other.ft
    def __eq__(self, other): return self.vetor == other.vetor
    def __ne__(self, other): return self.vetor != other.vetor
    def __add__(self, other): return self.ft + other.ft
    def __sub__(self, other): return self.ft - other.ft
    def __str__(self): return np.array2string(self.vetor)

    def fitness(self, weights):
        for (index, value) in enumerate(self.vetor):
            for arr in np.dot(weights[index], value):
                self.ft += np.sum(np.sum(arr))
        self.ft = self.ft/np.sum(self.vetor)


def desempenho(empresa):
    data = [
        np.array_split(empresa['Open'], 7), np.array_split(empresa['High'], 7),
        np.array_split(empresa['Low'], 7), np.array_split(empresa['Close'], 7),
        np.array_split(empresa['Adj Close'], 7), np.array_split(empresa['Volume'], 7)]
    return np.multiply(
        np.add(
            np.subtract(data[3], data[0]),
            np.subtract(data[1], data[2])),
        np.divide(
            data[5],
            np.subtract(
                data[3],
                data[4]
            )
        )
    )


def weigthEmpresas(empresas):
    weights = []
    for key in empresas:
        weights.append(desempenho(empresas[key]))
    return sorted(weights, key=len)


def fixSum(individuo):
    while(np.sum(individuo.vetor) != 1.0):
        dist = np.sum(individuo.vetor)
        if (dist > 1.0):
            individuo.vetor[np.argmax(individuo.vetor)] = 0.0
        elif(dist < 1.0):
            increase = 1.0 - dist
            individuo.vetor[random.randrange(len(individuo.vetor))] += increase


def geraIndividuo(qtdElementos, w):
    proporcoes = np.zeros(qtdElementos)
    for i in range(qtdElementos):
        proporcoes[i] = random.randrange(10)/100
    ind = Individuo(proporcoes)
    fixSum(ind)
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
    nindividuo = copy.deepcopy(individuo)
    for i in range(qtd_mutacoes):
        nindividuo.vetor[random.randrange(size-1)] = random.randrange(10)/100
    fixSum(nindividuo)
    return nindividuo


def mutaPopulacao(populacao, qtd):
    mortos = []
    escolhidos = []
    count = 0
    for i in random.choices(list(populacao.keys()), k=qtd):
        escolhidos.append(populacao[i])
    for individuo in escolhidos:
        nid = mutacao(individuo)
        if(str(nid) not in populacao):
            populacao[str(nid)] = nid
            count += 1
    for i in sorted(populacao.items(), key=lambda x: x[1], reverse=False)[:count]:
        mortos.append(i[1])
    for i in range(len(mortos)):
        del populacao[str(mortos[i])]


def selecionaPais(populacao, qtdpassos):
    random.seed(random.random())
    pais = []
    for element in sorted(populacao.items(), key=lambda x: x[1], reverse=True)[:2]:
        pais.append(element[1])
    # p0 = pais[0]
    # p1 = pais[1]
    # for i in range(qtdpassos):
    #     aux = populacao[random.choice(list(populacao.keys()))]
    #     if(aux.ft > p0.ft):
    #         p0 = aux
    #     elif(aux.ft > p1.ft):
    #         p1 = aux
    return pais


def cruzamento(mae, pai, w):
    random.seed(random.random())
    cortes = [random.randrange(len(mae.vetor)-1) for x in range(2)]
    cortes.sort()
    filhos = []
    partesMae = np.array_split(mae.vetor, cortes)
    partesPai = np.array_split(pai.vetor, cortes)
    filhos.append(Individuo(np.concatenate(
        (partesPai[0], partesMae[1], partesMae[2]))))
    filhos.append(Individuo(np.concatenate(
        (partesMae[0], partesPai[1], partesPai[2]))))
    filhos.append(Individuo(np.concatenate(
        (partesMae[0], partesPai[1], partesMae[2]))))
    filhos.append(Individuo(np.concatenate(
        (partesPai[0], partesMae[1], partesPai[2]))))
    filhos.append(Individuo(np.concatenate(
        (partesMae[0], partesMae[1], partesPai[2]))))
    filhos.append(Individuo(np.concatenate(
        (partesPai[0], partesPai[1], partesMae[2]))))
    for i in range(len(filhos)):
        fixSum(filhos[i])
        filhos[i].fitness(w)
    return filhos
