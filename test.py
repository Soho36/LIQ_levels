testlist = [-69.39, -144.01, 729.0, 519.0, 984.0, 235.0, -45.88, -339.46, 5, 45]
result = []

for i in testlist:
    if i > 0:
        result.append('profit')
    else:
        result.append('loss')

trades_count = len(result)
profitable_trades_count = result.count('profit')
loss_trades_count = result.count('loss')
win_percent = (profitable_trades_count * 100) / trades_count
loss_percent = (loss_trades_count * 100) / trades_count

print(f'Trades: {trades_count}')
print(f'Profitable trades: {profitable_trades_count} ({win_percent}%)')
print(f'Profitable trades: {loss_trades_count} ({loss_percent}%)')
