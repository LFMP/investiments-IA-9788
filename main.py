from src.simulator.util import simulator
from src.common.read_data import read_data2016
from src.AG.busca import buscaGenetica


def main():
  # Initializations
  data = read_data2016()
  initialBalance = 100000.00 * 4.038         # Cotação do Dólar em 04/01/2016
  weights = buscaGenetica()

  simulator(data, weights, initialBalance)
  

if __name__ == "__main__":
  main()
