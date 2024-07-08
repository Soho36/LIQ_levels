opened_long_trade_flag = False
opened_short_trade_flag = False
signal_series = rejection_signals_series_outside

for signal_index, (signal_value, price_level) in enumerate(signal_series):
    # LONG TRADES LOGIC
    if signal_value == 100 and longs_allowed and not opened_long_trade_flag:
        opened_long_trade_flag = True
        trades_counter += 1
        trade_direction.append('Long')
        signal_candle_date = (filtered_df_original.iloc[signal_index]['Date']).strftime('%Y-%m-%d')
        signal_candle_time = filtered_df_original.iloc[signal_index]['Time']
        signal_candle_low = round(filtered_df_original.iloc[signal_index]['Low'], 3)

        if use_level_price_as_entry:
            entry_price = price_level
        elif use_candle_close_as_entry:
            entry_price = round(filtered_df_original.iloc[signal_index]['Close'], 3)
        else:
            entry_price = None
            print("Choose entry type".upper())

        stop_loss_price = None
        take_profit_price = None

        if stop_loss_as_candle_min_max:
            stop_loss_price = (signal_candle_low - stop_loss_offset)
            take_profit_price = (((entry_price - stop_loss_price) * risk_reward_simulation) + entry_price) + stop_loss_offset
        elif stop_loss_price_as_dollar_amount:
            stop_loss_price = entry_price - rr_dollar_amount
            take_profit_price = entry_price + (rr_dollar_amount * risk_reward_ratio)
        elif stop_loss_as_plus_candle:
            stop_loss_price = (signal_candle_low - ((entry_price - signal_candle_low) * sl_offset_multiplier))
            take_profit_price = (((entry_price - stop_loss_price) * risk_reward_simulation) + entry_price)
        else:
            print('Stop loss condition is not properly defined')

        print('------------------------------------------------------------------------------------------')
        print(f'▲ ▲ ▲ OPEN LONG TRADE: ▲ ▲ ▲ {signal_candle_date} {signal_candle_time}')
        print(f'Entry price: {entry_price}')
        print(f'Take: {round(take_profit_price, 3)} ({risk_reward_simulation}RR)')
        print(f'Stop: {stop_loss_price}')
        print()

        for j in range(signal_index, len(filtered_df_original)):
            current_candle_date = (filtered_df_original.iloc[j]['Date']).strftime('%Y-%m-%d')
            current_candle_time = (filtered_df_original.iloc[j]['Time'])
            current_candle_open = filtered_df_original.iloc[j]['Open']
            current_candle_high = filtered_df_original.iloc[j]['High']
            current_candle_low = filtered_df_original.iloc[j]['Low']
            current_candle_close = filtered_df_original.iloc[j]['Close']

            print('Next candle: ', current_candle_date, current_candle_time, '|',
                  'O', current_candle_open, 'H', current_candle_high,
                  'L', current_candle_low, 'C', current_candle_close)

            if current_candle_open > stop_loss_price and current_candle_low > stop_loss_price:
                if current_candle_low <= stop_loss_price and current_candle_high >= take_profit_price:
                    trade_result_both.append(1)
                elif current_candle_low <= stop_loss_price:
                    trade_result.append((stop_loss_price - spread) - (entry_price + spread))
                    trade_result_longs.append((stop_loss_price - spread) - (entry_price + spread))
                    profit_loss_long_short.append('LongLoss')
                    print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date} {current_candle_time}')
                    print()
                    print(f'Trade Close Price: {round(stop_loss_price, 3)}')
                    opened_long_trade_flag = False
                    print(f'P/L: ${round((stop_loss_price - spread) - (entry_price + spread), 3)}')
                    print('------------------------------------------------------------------------------------------')
                    break
                elif current_candle_high >= take_profit_price:
                    trade_result.append(take_profit_price - (entry_price + spread))
                    trade_result_longs.append(take_profit_price - (entry_price + spread))
                    profit_loss_long_short.append('LongProfit')
                    print(f'○ ○ ○ Take profit hit ○ ○ ○ at {current_candle_date} {current_candle_time}')
                    print()
                    print(f'Trade Close Price: {round(take_profit_price, 3)}')
                    opened_long_trade_flag = False
                    print(f'P/L: ${round(take_profit_price - (entry_price + spread), 3)}')
                    print('------------------------------------------------------------------------------------------')
                    break
                else:
                    opened_long_trade_flag = True
            else:
                trade_result.append((stop_loss_price - spread) - (entry_price + spread))
                trade_result_longs.append((stop_loss_price - spread) - (entry_price + spread))
                profit_loss_long_short.append('LongLoss')
                print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date} {current_candle_time}')
                print()
                print(f'Trade Close Price: {round(stop_loss_price, 3)}')
                opened_long_trade_flag = False
                print(f'P/L: ${round((stop_loss_price - spread) - (entry_price + spread), 3)}')
                print('------------------------------------------------------------------------------------------')
                break
