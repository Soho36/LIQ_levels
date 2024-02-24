import talib
import numpy as np
import matplotlib.pyplot as plt
from Pattern_rec import filtered_by_date_dataframe


prices = filtered_by_date_dataframe['Close'].values

# prices = np.array([14, 12, 15, 14, 16, 18, 17, 15, 13, 12, 14, 12, 13, 12, 14, 15, 13, 15, 16, 16, 17, 15,
#                    17, 15, 14, 13, 15], dtype=np.float64)


time_period = 10

print(f'Prices: {prices}')
print()

swing_highs = talib.MAX(prices, time_period)
swing_lows = talib.MIN(prices, time_period)

print(f'Swing highs: {swing_highs}')
print(f'Swing lows: {swing_lows}')
print()



def plot_line_chart():
    plt.figure(figsize=(15, 8))
    plt.plot(prices, label='Prices', marker='o')
    plt.plot(swing_highs[:-1], label='Swing Highs', marker='v', linestyle='', color='green')
    plt.plot(swing_lows[:-1], label='Swing Lows', marker='^', linestyle='', color='red')
    plt.legend()


plot_line_chart()

plt.show()
