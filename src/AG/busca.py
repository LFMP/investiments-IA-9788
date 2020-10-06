from AG.util import cruzamento, selecionaPais
from . import util
from common.read_data import read_data2mov
from math import ceil


def buscaGenetica():
    data = read_data2mov()
    w = util.weigthEmpresas(data)
    lenIndividuos = len(data)
    populacao = {}
    util.geraPopulacao(40, lenIndividuos, populacao, w)
    for i in range(300):
        pais = selecionaPais(populacao, 20)
        filhos = cruzamento(populacao[pais[0]], populacao[pais[1]], w)
