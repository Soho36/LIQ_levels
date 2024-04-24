trade_is_open = False
for j in range(signal_index + 1, len(filtered_df_original)):
    ...

    if current_candle_high >= entry_price and trade_is_open is False:
        ...

        trade_is_open = True

    elif current_candle_low <= stop_loss_price and trade_is_open is True:
        ...

        break

    elif current_candle_high >= take_profit_price and trade_is_open is True:
        ...

        break

    else:
        trade_is_open = False