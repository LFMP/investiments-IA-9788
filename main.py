from src.simulator.util import simulator
from src.common.read_data import read_data2016
import numpy as np


def main():
  # Initializations
  data = read_data2016()
  initialBalance = 100000.00
  weights = {}
  companies = list(data.keys())
  for comp in companies:
    weights[comp] = .1

  simulator(data, weights, initialBalance)
  

if __name__ == "__main__":
  main()