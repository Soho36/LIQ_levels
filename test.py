import mplfinance as mpf
import yfinance as yf
import pandas as pd

df = yf.download("TSLA", start="2024-03-25", end="2024-03-27", interval='5m', progress=False)
print(df)
df.index = pd.to_datetime(df.index)


mpf.plot(df, type='candle', style='yahoo')