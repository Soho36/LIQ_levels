if signals is not None and not signals.empty:
    # Convert signals to NaN where there are no signals
    signals_with_nan = signals.where(signals != 0, np.nan)  # replace values where the condition is False
    # Add the signals as a subplot
    add_plots.append(mpf.make_addplot(signals_with_nan, type='scatter', markersize=1000, marker='+', panel=0))
# Plot candlestick chart with additional plot
mpf.plot(df, type='candle', figsize=(15, 8), title=f'{file_path}'.upper(), ylabel='Price', addplot=add_plots)
print('Signals are plotted to candlestick chart')

