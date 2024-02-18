import pandas as pd
import mplfinance as mpf

# Sample data
data = {
    'Date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04'],
    'Open': [100, 110, 105, 120],
    'High': [120, 115, 115, 125],
    'Low': [90, 105, 100, 110],
    'Close': [110, 105, 110, 115]
}
df = pd.DataFrame(data)
print(df)
# Convert 'Date' column to datetime
df['Datetime'] = pd.to_datetime(df['Date'])
print(df)
df.set_index('Datetime', inplace=True)

# Create an additional plot (line plot of 'Close' prices)
add_plot = mpf.make_addplot(df['Close'])

# Plot candlestick chart with the additional plot
mpf.plot(df, type='candle', addplot=add_plot)
