import numpy as np

# Sample price and volume data
close_prices = np.array([10, 12, 11, 15, 14])
high_prices = np.array([11, 13, 12, 16, 15])
low_prices = np.array([9, 11, 10, 14, 13])
volume = np.array([1000, 1500, 1200, 2000, 1800])

# Calculate typical price
typical_price = (high_prices + low_prices + close_prices) / 3
print(typical_price)

# Calculate cumulative sum of (typical price * volume)
cumulative_tp_volume = np.cumsum(typical_price * volume)

# Calculate cumulative volume
cumulative_volume = np.cumsum(volume)

# Calculate VWAP
vwap = cumulative_tp_volume / cumulative_volume

print(vwap)
