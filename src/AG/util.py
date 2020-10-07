import random
import numpy as np
import copy
from math import ceil


class Individuo:
    def __init__(self, vetor, ft=0):
        self.vetor = vetor
        self.ft = ft

    def __lt__(self, other): return self.ft > other.ft
    def __gt__(self, other): return self.ft < other.ft
    def __eq__(self, other): return self.ft == other.ft
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
            discount = dist - 1.0
            for (index, value) in enumerate(individuo.vetor):
                if(value >= discount):
                    individuo.vetor[index] = value - discount
                    break
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


def mutaPopulacao(populacao, qtd):
    random.seed(random.random())
    mortos = []
    for i in random.choices(list(populacao.keys()), k=qtd):
        mortos.append(populacao[i])
    escolhidos = copy.deepcopy(mortos)
    for individuo in mortos:
        if str(individuo) in populacao:
            del populacao[str(individuo)]
    for individuo in escolhidos:
        mutacao(individuo)
        populacao[str(individuo)] = individuo


def mutacao(individuo):
    size = len(individuo.vetor)
    qtd_mutacoes = random.randrange(ceil(size/3))
    random.seed(random.random())
    for i in range(qtd_mutacoes):
        individuo.vetor[random.randrange(size-1)] = random.randrange(10)/100
    fixSum(individuo)


def selecionaPais(populacao, qtdpassos):
    random.seed(random.random())
    p0 = populacao[random.choice(list(populacao.keys()))]
    p1 = populacao[random.choice(list(populacao.keys()))]
    for i in range(qtdpassos):
        aux = populacao[random.choice(list(populacao.keys()))]
        if(aux.ft > p0.ft):
            p0 = aux
        elif(aux.ft > p1.ft):
            p1 = aux
    return [p0, p1]


def cruzamento(mae, pai, w, qtdFIlhos=6):
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
    for i in range(qtdFIlhos):
        fixSum(filhos[i])
        filhos[i].fitness(w)
    return filhos
