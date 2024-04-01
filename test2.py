import mplfinance as mpf
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

# Download data
df = yf.download("AAPL", start="2024-03-20", end="2024-03-27", interval='5m', progress=False)
df.index = pd.to_datetime(df.index)
print(df)

# Extract data for open and max lines
o_lines = [(df.index[0], df['Open'].iloc[0]), (df.index[-1], df['Open'].iloc[0])]
m_lines = [(df['High'].idxmax(), df['High'].max()), (df.index[-1], df['High'].max())]
b_lines = [(df['Low'].idxmin(), df['Low'].min()), (df.index[-1], df['Low'].min())]

lines_dict = [o_lines, m_lines, b_lines]
print(lines_dict)

# Plot candlestick chart with additional lines
mpf.plot(df, type='candle', figsize=(12, 6),
         alines=dict(alines=lines_dict, linewidths=2, alpha=0.4),
         style='yahoo')
