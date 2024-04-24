# SHORT TRADES LOGIC
            elif signal == -100 and shorts_allowed:
                counter += 1
                trade_direction.append('Short')
                signal_candle_date = (filtered_df_original.iloc[signal_index]['Date']).strftime('%Y-%m-%d')
                signal_candle_time = filtered_df_original.iloc[signal_index]['Time']
                signal_candle_high = round(filtered_df_original.iloc[signal_index]['High'], 3)
                entry_price = None

                if use_candle_close_as_entry:
                    entry_price = round(filtered_df_original.iloc[signal_index]['Close'], 3)   # ENTRY

                elif use_candle_high_or_low_as_entry:
                    entry_price = round(filtered_df_original.iloc[signal_index]['Low'], 3)

                else:
                    print("Choose entry type".upper())

                stop_loss_price = None
                take_profit_price = None

                if stop_loss_as_candle_high_low:
                    stop_loss_price = signal_candle_high + stop_loss_offset
                    take_profit_price = ((entry_price -
                                          ((stop_loss_price - entry_price)
                                           * risk_reward_simulation))) - stop_loss_offset

                else:
                    print('Stop loss condition is not properly defined')

                print('------------------------------------------------------------------------------------------')
                print(f'▼ ▼ ▼ OPEN SHORT TRADE: ▼ ▼ ▼ {signal_candle_date} {signal_candle_time}')
                print(f'Entry price: {entry_price}')
                print(f'Stop: {stop_loss_price}')
                print(f'Take: {round(take_profit_price, 3)} ({risk_reward_simulation}RR)')
                print()
                # print(f'Current (signal) candle OHLC | O {signal_candle_open}, H {signal_candle_high}, '
                #       f'L {signal_candle_low}, C {entry_price}')

                for j in range(signal_index, len(filtered_df_original)):
                    current_candle_date = (filtered_df_original.iloc[j]['Date']).strftime('%Y-%m-%d')
                    current_candle_time = (filtered_df_original.iloc[j]['Time'])
                    current_candle_open = filtered_df_original.iloc[j]['Open']
                    current_candle_high = filtered_df_original.iloc[j]['High']
                    current_candle_low = filtered_df_original.iloc[j]['Low']
                    current_candle_close = filtered_df_original.iloc[j]['Close']

                    print('Next candle: ', current_candle_date, current_candle_time, '|',
                          'O', current_candle_open,
                          'H', current_candle_high,
                          'L', current_candle_low,
                          'C', current_candle_close)

                    if current_candle_open < stop_loss_price and current_candle_high < stop_loss_price:

                        elif current_candle_high >= stop_loss_price:
                            trade_result.append((entry_price - spread) -
                                                (stop_loss_price + spread))
                            trade_result_shorts.append((entry_price - spread) -
                                                       (stop_loss_price + spread))
                            profit_loss_long_short.append('ShortLoss')
                            print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date} {current_candle_time}')
                            print()
                            print(f'Trade Close Price: {round(stop_loss_price, 3)}')
                            print(
                              f'P/L: ${round((entry_price - spread) - (stop_loss_price + spread), 3)}'
                            )
                            print(
                                '---------------------------------------------'
                                '---------------------------------------------'
                            )
                            break

                        elif current_candle_low <= take_profit_price:
                            trade_result.append((entry_price - spread) - take_profit_price)
                            trade_result_shorts.append((entry_price - spread) - take_profit_price)
                            profit_loss_long_short.append('ShortProfit')
                            print(f'○ ○ ○ Take profit hit ○ ○ ○ at {current_candle_date} {current_candle_time}')
                            print()
                            print(f'Trade Close Price: {round(take_profit_price, 3)}')
                            print(f'P/L: ${round((entry_price - spread) - take_profit_price, 3)}')
                            print(
                                '---------------------------------------------'
                                '---------------------------------------------'
                            )

                            break

                        else:
                            pass