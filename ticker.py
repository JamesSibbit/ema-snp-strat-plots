from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np

# Apple, Microsoft and the S&P500 index.
tickers = ['AAPL', 'MSFT', '^GSPC']

start_date = '2010-01-01'
end_date = '2020-07-01'

panel_data = web.DataReader(tickers, 'yahoo', start_date, end_date)

close = panel_data['Close']

weekdays = pd.date_range(start = start_date, end = end_date, freq = 'B')
close = close.reindex(weekdays)

#Create Close df with only weekday values
close = close.fillna(method = 'bfill')

#Create SMA for Apple stock (20 day)

print(close.tail())

appl = close.loc[:, 'AAPL']

twenty_roll_appl = appl.rolling(window = 20).mean()
hun_roll_appl = appl.rolling(window = 100).mean()
twohun_roll_appl = appl.rolling(window = 200).mean()

#Now plot our SMA for close of AAPL stock with 20, 100 and 200 day rolling windows

# fig, ax = plt.subplots(figsize = (16,9))
# ax.plot(appl.index, appl, label = "AAPL")
# ax.plot(twenty_roll_appl.index, twenty_roll_appl, label = "20 day SMA")
# ax.plot(hun_roll_appl.index, hun_roll_appl, label = "100 day SMA")
# ax.plot(twohun_roll_appl.index, twohun_roll_appl, label = "200 day SMA")
#
# ax.set_xlabel('Date')
# ax.set_ylabel('Closing price ($)')
# ax.legend()
#
# plt.show()

# Want to move onto considering returns and using the above to create a trading strategyself.

#First, consider usual returns

ret = close.pct_change(1)

#Now log returns

log_ret = np.log(close).diff()

#Now compare log returns in apple, microsoft and S&P

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,12))

for c in log_ret:
    ax1.plot(log_ret.index, log_ret[c].cumsum(), label=str(c))

ax1.set_ylabel('Cum log returns')
ax1.legend(loc='best')

for c in log_ret:
    ax2.plot(log_ret.index, 100*(np.exp(log_ret[c].cumsum()) - 1), label=str(c))

ax2.set_ylabel('Total rel returns (%)')
ax2.legend(loc='best')

# We now use pandas to calculate EMA

ema_twenty = close.ewm(span = 20, adjust=False).mean()

ema_twenty_appl = appl.ewm(span = 20, adjust=False).mean()

# print(ema_twenty.head())

fig, ax = plt.subplots(figsize = (16,9))
ax.plot(appl.index, appl, label = "AAPL")
ax.plot(twenty_roll_appl.index, twenty_roll_appl, label = "20 day SMA")
ax.plot(ema_twenty_appl.index, ema_twenty_appl, label = "20 day EMA")


ax.set_xlabel('Date')
ax.set_ylabel('Closing price ($)')
ax.legend()

# plt.show()

#We now use our EMA to create a strategy. If underlying crosses EMA from below, we close out any short position and go long in the stock, if it crosses from above we close out long & go short. We assume an equal split between S&P, MSFT & AAPL.

raw = close - ema_twenty
position = ((1/3)*raw.apply(np.sign)).shift(1)

#If we have a change of sign from positive to negative, means EMA crosses over close from below, so we go short (and vice versa for negative to positive).

print(raw.tail())
print(position.tail())

#Now see what our signal does for eg. Microsoft over the past however long

start_daten = '2020-01-01'
end_daten = '2020-07-01'

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,9))

ax1.plot(close.loc[start_daten:end_daten, :].index, close.loc[start_daten:end_daten, 'MSFT'], label='Price')
ax1.plot(ema_twenty.loc[start_daten:end_daten, :].index, ema_twenty.loc[start_daten:end_daten, 'MSFT'], label = 'Span 20-days EMA')

ax1.set_ylabel('$')
ax1.legend(loc='best')

ax2.plot(position.loc[start_daten:end_daten, :].index, position.loc[start_daten:end_daten, 'MSFT'],
        label='Trading position')

ax2.set_ylabel('Trading position')

plt.show()
