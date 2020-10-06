import numpy as np

def initWallets(companies: list, weights: dict, initialBalance: int):
  splittedWallet = {}
  investedWallet = {}
  for comp in companies:
    splittedWallet[comp] = weights[comp] * initialBalance
    investedWallet[comp] = 0
  return splittedWallet, investedWallet

def simulator(data: dict, weights: dict, initialBalance: int):
  # Initializing Wallets
  companies = list(weights.keys())
  splittedWallet, investedWallet = initWallets(companies, weights, initialBalance)

  # monthlyBalance = [{} for _ in range(12)]

  # Daily loop
  dateList = data[companies[0]]['Date']
  for date in dateList:
    # month = int(date.split('-')[1])
    # monthlyBalance[month-1] = 
    for comp in companies:
      pass

  

    
    

  