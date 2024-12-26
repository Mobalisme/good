import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

tickers = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL']
_BILLION = 1000 * 1000 * 1000

net_income_d = {}
for ticker in tickers:
  yf_ticker = yf.Ticker(ticker)
  net_income_d[ticker] = yf_ticker.income_stmt.loc['Net Income'] / _BILLION
net_income = pd.concat(net_income_d, axis = 1).astype(float)

sns.set_style('whitegrid')
ax = net_income.plot(marker = 'o')
plt.gca().set_prop_cycle(None)
net_income_interpolated = net_income.interpolate(
    method = 'time', limit_direction = 'backward')
net_income_interpolated.plot(ax = ax, lw = 1, ls = '--', legend = False)
plt.ylabel('Net Income (Billion dollars)')
plt.show()
