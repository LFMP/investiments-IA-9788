import numpy as np
import pandas as pd
import ta
from collections import Counter
from copy import deepcopy

def calcIndicators(data: dict, company: str):
  high = data[company]['High']
  low = data[company]['Low']
  close = data[company]['Close']
  adaptedData = [[high[i], low[i], close[i]] for i in range(len(high))]
  df = pd.DataFrame(adaptedData, columns=['High', 'Low', 'Close'])
  stochSignal = ta.momentum.stoch_signal(df['High'], df['Low'], df['Close'])
  rsi = ta.momentum.rsi(df['Close'])
  return list(stochSignal), list(rsi)

def initWallets(companies: list, weights: dict, initialBalance: int):
  initialWallet = {}
  splittedWallet = {}
  investedWallet = {}
  initialInvested = {}
  for comp in companies:
    initialWallet[comp] = weights[comp] * initialBalance
    splittedWallet[comp] = weights[comp] * initialBalance
    investedWallet[comp] = 0
    initialInvested[comp] = 0
  return initialWallet, splittedWallet, investedWallet, initialInvested

def totalProfit(companies: list, startWallet: dict, endWallet: dict):
  initialBalance = sum(startWallet.values())
  finalBalance = sum(endWallet.values())
  profit = finalBalance - initialBalance
  profitPC = profit / initialBalance * 100
  return {'initialBalance': initialBalance,
          'finalBalance': finalBalance,
          'profit': profit,
          'profitPC': profitPC}

def mostLeastProfitComp(companies: list, startWallet: dict, endWallet: dict):
  first = True
  for comp in companies:
    profit = endWallet[comp] - startWallet[comp]
    profitPC = profit / startWallet[comp] * 100
    if first:
      mostProfitComp = comp
      mostProfit = profit
      mostProfitPC = profitPC
      leastProfitComp = comp
      leastProfit = profit
      leastProfitPC = profitPC
      first = False
    else:
      if profitPC > mostProfitPC:
        mostProfitComp = comp
        mostProfit = profit
        mostProfitPC = profitPC
      elif profitPC < leastProfitPC:
        leastProfitComp = comp
        leastProfit = profit
        leastProfitPC = profitPC
  return {'mostProfitComp': mostProfitComp,
          'mostProfit': mostProfit,
          'mostProfitPC': mostProfitPC,
          'leastProfitComp': leastProfitComp,
          'leastProfit': leastProfit,
          'leastProfitPC': leastProfitPC}
  
def printInfos(i: int, companies: list, splittedWallet1: dict, investedWallet1: dict, splittedWallet2: dict, investedWallet2: dict):
  print("------------- Resultado Mês", i, "-------------")
  print()
  balanceInfos = totalProfit(companies, dict(Counter(splittedWallet1) + Counter(investedWallet1)), dict(Counter(splittedWallet2) + Counter(investedWallet2)))
  print("Saldo inicial: \tR${:.2f}" .format(balanceInfos['initialBalance']))
  print("Saldo final: \tR${:.2f}" .format(balanceInfos['finalBalance']))
  print("Variação: \tR${:.2f} ({:.2f}%)" .format(balanceInfos['profit'], balanceInfos['profitPC']))
  compInfos = mostLeastProfitComp(companies, dict(Counter(splittedWallet1) + Counter(investedWallet1)), dict(Counter(splittedWallet2) + Counter(investedWallet2)))
  print("Empresa mais lucrativa: ", compInfos['mostProfitComp'], "-> R${:.2f} ({:.2f}%)" .format(compInfos['mostProfit'], compInfos['mostProfitPC']))
  print("Empresa menos lucrativa:", compInfos['leastProfitComp'], "-> R${:.2f} ({:.2f}%)" .format(compInfos['leastProfit'], compInfos['leastProfitPC']))
  print()

def simulator(data: dict, weights: dict, initialBalance: int):
  # Initializing Wallets
  companies = list(weights.keys())
  initialWallet, splittedWallet, investedWallet, initialInvested = initWallets(companies, weights, initialBalance)
  currentPrice = {}

  monthlyBalance = [{} for _ in range(12)]
  monthlyInvested = [{} for _ in range(12)]

  # Calc Stoch Signal
  for comp in companies:
    stochSignal, rsi = calcIndicators(data, comp)
    data[comp]['StochSignal'] = stochSignal
    data[comp]['RSI'] = rsi

  # Daily loop
  dateList = data[companies[0]]['Date']
  for i in range(len(dateList)):
    if data[companies[0]]['StochSignal'][i] != 'nan':
      for comp in companies:

        # Doing stocks exchanges
        ssi = data[comp]['StochSignal'][i]
        rsi = data[comp]['RSI'][i]
        if ssi < 20 and rsi < 30:
          ssiBuy = (20-ssi)/20
          rsiBuy = (30-rsi)/30
          exchangeMoney = (ssiBuy + rsiBuy)/2 * splittedWallet[comp]
          splittedWallet[comp] -= exchangeMoney
          investedWallet[comp] += exchangeMoney
        elif ssi > 80 and rsi > 70:
          ssiSell = (ssi-80)/20
          rsiSell = (rsi-70)/30
          exchangeMoney = (ssiSell + rsiSell)/2 * investedWallet[comp]
          investedWallet[comp] -= exchangeMoney
          splittedWallet[comp] += exchangeMoney

        # Updating stocks values
        if i > 0:
          newPrice = data[comp]['Close'][i]
          investedWallet[comp] = (investedWallet[comp] / currentPrice[comp]) * newPrice

        currentPrice[comp] = data[comp]['Close'][i]

      date = dateList[i]
      month = int(date.split('-')[1])
      monthlyBalance[month-1] = deepcopy(splittedWallet)
      monthlyInvested[month-1] = deepcopy(investedWallet)
    else:
      for comp in companies:
        currentPrice[comp] = data[comp]['Close'][i]

  # Printing monthly results
  for month in range(12):
    if month == 0:
      printInfos(month+1, companies, initialWallet, initialInvested, monthlyBalance[0], monthlyInvested[0])
    else:
      printInfos(month+1, companies, monthlyBalance[month-1], monthlyInvested[month-1], monthlyBalance[month], monthlyInvested[month])

  # Printing final results
  print("=============== Resultado final ===============")
  print()
  balanceInfos = totalProfit(companies, initialWallet, dict(Counter(splittedWallet) + Counter(investedWallet)))
  print("Saldo inicial: \tR${:.2f}" .format(balanceInfos['initialBalance']))
  print("Saldo final: \tR${:.2f}" .format(balanceInfos['finalBalance']))
  print("Variação: \tR${:.2f} ({:.2f}%)" .format(balanceInfos['profit'], balanceInfos['profitPC']))
  compInfos = mostLeastProfitComp(companies, initialWallet, dict(Counter(splittedWallet) + Counter(investedWallet)))
  print("Empresa mais lucrativa: ", compInfos['mostProfitComp'], "-> R${:.2f} ({:.2f}%)" .format(compInfos['mostProfit'], compInfos['mostProfitPC']))
  print("Empresa menos lucrativa:", compInfos['leastProfitComp'], "-> R${:.2f} ({:.2f}%)" .format(compInfos['leastProfit'], compInfos['leastProfitPC']))
  
  