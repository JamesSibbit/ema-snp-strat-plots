from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np

today = datetime.date.today() - datetime.timedelta(days=1)
last_month = today - datetime.timedelta(days=31)

panel_data = web.DataReader("^GSPC", 'yahoo', last_month, today)

close = panel_data['Close']

weekdays = pd.date_range(start = last_month, end = today, freq = 'B')

close = close.reindex(weekdays)

close = close.fillna(method = 'bfill')

ema_five = close.ewm(span = 5, adjust=False).mean()

raw = close - ema_five
position = raw.apply(np.sign).shift(1)

fig, (ax1,ax2) = plt.subplots(2,1, figsize = (16,9))

ax1.plot(close.index, close, label="Close Price")
ax1.plot(ema_five.index, ema_five, label="5-day EMA")

ax1.set_ylabel('$')
ax1.legend(loc = 'best')

ax2.plot(position.index, position, label = "Position")
ax2.set_ylabel("Position")

plt.show()
