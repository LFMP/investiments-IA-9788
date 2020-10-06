from AG.util import cruzamento, geraPopulacao, mutaPopulacao, selecionaPais, weigthEmpresas
from common.read_data import read_data2mov


def buscaGenetica():
    data = read_data2mov()
    w = weigthEmpresas(data)
    lenIndividuos = len(data)
    populacao = {}
    geraPopulacao(40, lenIndividuos, populacao, w)
    for i in range(300):
        pais = selecionaPais(populacao, 20)
        filhos = cruzamento(populacao[pais[0]], populacao[pais[1]], w)
        melhores = sorted(populacao, key=populacao.get, reverse=True)[:10]
        for f in filhos:
            for m in melhores:
                if(f.ft > m.ft):
                    try:
                        del populacao[str(m.vetor)]
                        populacao[str(f.vetor)] = f
                    except Exception:
                        print('deu merda')
        mutaPopulacao(populacao, len(populacao)/10)
    print(max(populacao, key=lambda key: populacao[key]))
