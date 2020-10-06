import random
import numpy as np
import copy
from math import ceil


class Individuo:
    def __init__(self, vetor, ft=0):
        self.vetor = vetor
        self.ft = ft

    def __lt__(self, other): return self.ft > other.ft
    def __eq__(self, other): return self.ft == other.ft
    def __str__(self): return str(self.vetor)

    def fitness(self, weights):
        for (index, value) in enumerate(self.vetor):
            self.ft += np.sum(np.multiply(weights[index], value))
        self.ft = self.ft/np.sum(self.vetor)


def desempenho(empresa):
    data = [
        np.array_split(empresa['Open'], 7), np.array_split(empresa['High'], 7),
        np.array_split(empresa['Low'], 7), np.array_split(empresa['Close'], 7),
        np.array_split(empresa['Adj Close'], 7), np.array_split(empresa['Volume'], 7)]
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


def mutaPopulacao(populacao, qtd):
    random.seed(random.random())
    mortos = random.choices(populacao, k=qtd)
    escolhidos = copy.deepcopy(mortos)
    for individuo in mortos:
        del populacao[str(individuo)]
    for individuo in escolhidos:
        mutacao(individuo)
        populacao[str(individuo.vetor)] = individuo


def mutacao(individuo):
    size = len(individuo.vetor)
    qtd_mutacoes = random.randrange(ceil(size/3))
    random.seed(random.random())
    for i in range(qtd_mutacoes):
        individuo.vetor[random.randrange(size-1)] = random.randrange(100)/100
    fixSum(individuo)


def selecionaPais(populacao, qtdpassos):
    pais = []
    random.seed(random.random())
    p0 = random.choice(populacao)
    p1 = random.choice(populacao)
    for i in range(qtdpassos):
        aux = random.choice(populacao)
        if(aux.ft > p0.ft):
            p0 = aux
        elif(aux.ft > p1.ft):
            p1 = aux
    pais.append(str(p0.vetor))
    pais.append(str(p1.vetor))
    return pais


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
