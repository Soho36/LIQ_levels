import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
from Pattern_rec_BACKTEST import vw_points_series_outside

# Sample DataFrame with OHLC data
data = {
    'Date': pd.date_range(start='2022-01-01', periods=100),
    'Open': np.random.rand(100) * 100,
    'High': np.random.rand(100) * 100,
    'Low': np.random.rand(100) * 100,
    'Close': np.random.rand(100) * 100,
    'Volume': np.random.randint(1000, 10000, size=100)
}
df = pd.DataFrame(data)
df.set_index('Date', inplace=True)

# Calculate moving average
window = 20
# moving_average = df['Close'].rolling(window=window).mean()
moving_average = vw_points_series_outside
print(moving_average)

# Plot candlestick chart with moving average
mpf.plot(df, type='candle', style='yahoo', title='Candlestick Chart with Moving Average',
         ylabel='Price', ylabel_lower='Volume',
         mav=(window,),  # Plot moving average
         figsize=(12, 6))

# Show the plot
plt.show()
