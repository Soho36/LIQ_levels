import talib
import pandas as pd
import matplotlib.pyplot as plt

# Example: Create a sample DataFrame with historical stock prices
data = {'Close': [100, 105, 98, 110, 102, 108, 95, 115, 112, 120]}
df = pd.DataFrame(data)

# Calculate the Double Top and Double Bottom patterns
double_top = talib.CDLDOJI(df['Close'])
double_bottom = talib.CDLDOJISTAR(df['Close'])

# Print the signals
print("Double Top Signal:", double_top)
print("Double Bottom Signal:", double_bottom)

# Plot the stock prices with signals
plt.figure(figsize=(10, 5))
plt.plot(df['Close'], label='Stock Prices', marker='o')
plt.title('Stock Prices with Double Top and Double Bottom Signals')
plt.xlabel('Days')
plt.ylabel('Price')
plt.legend()

# Highlight Double Top signals with red triangles
for i, signal in enumerate(double_top):
    if signal > 0:
        plt.annotate('Double Top', xy=(i, df['Close'][i]), xytext=(i, df['Close'][i] + 5),
                     arrowprops=dict(facecolor='red', arrowstyle='->'))

# Highlight Double Bottom signals with green triangles
for i, signal in enumerate(double_bottom):
    if signal > 0:
        plt.annotate('Double Bottom', xy=(i, df['Close'][i]), xytext=(i, df['Close'][i] - 5),
                     arrowprops=dict(facecolor='green', arrowstyle='->'))

plt.show()
