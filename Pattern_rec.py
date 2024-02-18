import talib
import pandas as pd
import os
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
# ------------------------------------------
# The list of paths to datafiles:
# file_path = 'TXT/merged_data.csv'
# file_path = 'TXT/exel.csv'
# file_path = 'TXT/spr.csv'
# file_path = 'TXT/zim.csv'
# file_path = 'TXT/extr.csv'
# file_path = 'TXT/aehr.csv'
# file_path = 'TXT/tsla_D1.csv'
# file_path = 'TXT/neog_D1.csv'
# file_path = 'TXT/meta_D1.csv'
# file_path = 'TXT/tsla_m5.csv'
# file_path = 'TXT/tsla_m1.csv'
file_path = 'TXT/MT4/BTCUSD_D1.csv'
# file_path = 'TXT/MT4/BTCUSD_m60.csv'
# file_path = 'TXT/MT4/BTCUSD_m5.csv'
# ------------------------------------------
# pd.set_option('display.max_columns', 10)  # Uncomment to display all columns


# ******************************************************************************
start_date = '2017-04-18'     # Choose the start date to begin from
end_date = '2017-10-06'     # Choose the end date
code_of_pattern = 18     # Choose the index of pattern (from Ta-lib patterns.csv)
risk_reward_ratio = 2   # Chose risk/reward ratio (how much you are aiming to win compared to lose)
stop_loss_offset = 0    # Place stop with offset from original price
# ******************************************************************************


def getting_dataframe_from_file(path):

    directory_path = 'TXT/'
    print()
    print('Datafiles in folder: ')
    for filename in os.listdir(directory_path):     # Making a list of files located in TXT folder
        print(filename)
    print()
    print(f'Current file is: {path}')

    columns_to_parce = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Filename']

    #  for MT4 files set dayfirst=False
    csv_df = pd.read_csv(path, parse_dates=[0], dayfirst=False, usecols=columns_to_parce)
    print()
    print(f'Dataframe derived from CSV:\n {csv_df}')
    print()
    return csv_df


dataframe_from_csv = getting_dataframe_from_file(file_path)


def date_range_func(df, start, end):

    on_off = True

    if on_off:
        date_range = pd.date_range(start=start, end=end, freq='D')
        # print('Date range: \n', list(date_range))

        date_column = df['Date']        # Select the 'Date' column from the DataFrame
        dates_in_range = date_column.isin(date_range)   # checks which dates from date_column fall within the generated
        # date range, resulting in a boolean mask

        df_filtered_by_date = df[dates_in_range]
        if df_filtered_by_date.empty:
            # print('NB! Dataframe is empty, check the date range!')
            raise ValueError('NB! Dataframe is empty, check the date range!')
        else:
            return df_filtered_by_date


filtered_by_date_dataframe = date_range_func(dataframe_from_csv, start_date, end_date)
print()
print(f'Dataframe filtered by date:\n {filtered_by_date_dataframe.head()}')
print()
print('************************************TRADES SIMULATION************************************')

#  ----------------------------------------------
#  PATTERN RECOGNITION
#  ----------------------------------------------

patterns_dataframe = pd.read_csv('Ta-lib patterns.csv')


def pattern_recognition_func(patterns_df, code):  # Reading Pattern codes from CSV

    pattern_code = patterns_df['PatternCode'].iloc[code]
    pattern_name = patterns_df['PatternName'].iloc[code]
    pattern_index = patterns_df.index[code]
    print()
    print(f'Current Pattern is: {pattern_code}, {pattern_name}, {pattern_index}')

    pattern_function = getattr(talib, pattern_code)
    signal = pattern_function(filtered_by_date_dataframe['Open'], filtered_by_date_dataframe['High'],
                              filtered_by_date_dataframe['Low'], filtered_by_date_dataframe['Close'])

    return signal


recognized_pattern = pattern_recognition_func(patterns_dataframe, code_of_pattern)  # Returns series
# print(recognized_pattern)


#  ----------------------------------------------
#  TRADES SIMULATION
#  ----------------------------------------------


def trades_simulation(filtered_df, risk_reward, sl_offset):
    on_off = True
    if on_off:
        trades_counter = 0
        trade_result = []
        for signal_index, signal_value in enumerate(recognized_pattern):

            # LONG TRADES LOGIC
            if signal_value == 100:
                trades_counter += 1
                signal_candle_date = filtered_df.iloc[signal_index]['Date']
                signal_candle_close_entry = round(filtered_df.iloc[signal_index]['Close'], 2)
                signal_candle_low = round(filtered_df.iloc[signal_index]['Low'], 2)
                stop_loss_price = signal_candle_low - sl_offset
                take_profit_price = (
                        round((signal_candle_close_entry - signal_candle_low) * risk_reward) +
                        signal_candle_close_entry)
                print('------------------------------------------------------------------------------------------')
                print(f'▲ ▲ ▲ OPEN LONG TRADE: ▲ ▲ ▲ {signal_candle_date}')
                print(f'Entry price: {signal_candle_close_entry}')
                print(f'Take: {round(take_profit_price, 2)} ({risk_reward}RR)')
                print(f'Stop: {stop_loss_price} ({signal_candle_low} - {sl_offset})')
                print()

                for j in range(signal_index + 1, len(filtered_df)):
                    current_candle_date = filtered_df.iloc[j]['Date']
                    current_candle_open = filtered_df.iloc[j]['Open']
                    current_candle_high = filtered_df.iloc[j]['High']
                    current_candle_low = filtered_df.iloc[j]['Low']
                    current_candle_close = filtered_df.iloc[j]['Close']

                    print('Current candle: ', current_candle_date, '|',
                          'O', current_candle_open,
                          'H', current_candle_high,
                          'L', current_candle_low,
                          'C', current_candle_close)

                    if current_candle_high >= take_profit_price:
                        trade_result.append(take_profit_price - signal_candle_close_entry)
                        print(f'○ ○ ○ Take profit hit ○ ○ ○ at {current_candle_date}')
                        print()
                        print(f'Close price: {round(take_profit_price, 2)}')
                        print(f'P/L: ${round(take_profit_price - signal_candle_close_entry, 2)}')
                        print(
                            '------------------------------------------------------------------------------------------'
                        )
                        break
                    elif current_candle_low <= stop_loss_price:
                        trade_result.append(stop_loss_price - signal_candle_close_entry)
                        print(f'● ● ● Stop Loss hit ● ● ● at {current_candle_date}')
                        print()
                        print(f'Close price: {round(stop_loss_price, 2)}')
                        print(f'P/L: ${round(stop_loss_price - signal_candle_close_entry, 2)}')
                        print(
                            '------------------------------------------------------------------------------------------'
                        )
                        break
                    else:
                        pass
                        # print('Still Open')

            # SHORT TRADES LOGIC
            elif signal_value == -100:
                trades_counter += 1
                signal_candle_date = filtered_df.iloc[signal_index]['Date']
                signal_candle_close_entry = round(filtered_df.iloc[signal_index]['Close'], 2)
                signal_candle_high = round(filtered_df.iloc[signal_index]['High'], 2)
                stop_loss_price = signal_candle_high + sl_offset
                take_profit_price = (
                        signal_candle_close_entry - round((signal_candle_high - signal_candle_close_entry)
                                                          * risk_reward))
                print('------------------------------------------------------------------------------------------')
                print(f'▼ ▼ ▼ OPEN SHORT TRADE: ▼ ▼ ▼ {signal_candle_date}')
                print(f'Entry price: {signal_candle_close_entry}')
                print(f'Stop: {stop_loss_price} ({signal_candle_high} + {sl_offset})')
                print(f'Take: {round(take_profit_price, 2)} ({risk_reward}RR)')
                print()

                for j in range(signal_index + 1, len(filtered_df)):
                    current_candle_date = filtered_df.iloc[j]['Date']
                    current_candle_open = filtered_df.iloc[j]['Open']
                    current_candle_high = filtered_df.iloc[j]['High']
                    current_candle_low = filtered_df.iloc[j]['Low']
                    current_candle_close = filtered_df.iloc[j]['Close']

                    print('Current candle: ', current_candle_date, '|',
                          'O', current_candle_open,
                          'H', current_candle_high,
                          'L', current_candle_low,
                          'C', current_candle_close)
                    if current_candle_low <= take_profit_price:
                        print(f'○ ○ ○ Take profit hit ○ ○ ○ at {current_candle_date}')
                        print()
                        print(f'Close price: {round(take_profit_price, 2)}')
                        print(f'P/L: ${round(signal_candle_close_entry - take_profit_price, 2)}')
                        print(
                            '------------------------------------------------------------------------------------------'
                        )
                        trade_result.append(signal_candle_close_entry - take_profit_price)
                        break
                    elif current_candle_high >= stop_loss_price:
                        print(f'● ● ● Stop Loss hit ● ● ● at {current_candle_date}')
                        print()
                        print(f'Close price: {round(stop_loss_price, 2)}')
                        print(f'P/L: ${round(signal_candle_close_entry - stop_loss_price, 2)}')
                        print(
                            '------------------------------------------------------------------------------------------'
                        )
                        trade_result.append(signal_candle_close_entry - stop_loss_price)
                        break
                    else:
                        pass

        return trade_result, trades_counter


trade_results_to_trade_analysis, trades_counter_to_trade_analysis = (
    trades_simulation(filtered_by_date_dataframe, risk_reward_ratio, stop_loss_offset))


def trades_analysis(trade_result, trades_counter):

    print()
    print('************************************TRADES ANALYSIS************************************')
    print()
    print(f'Trades count: {trades_counter}')

    if trades_counter == 0:
        print("No trades were placed! Try other pattern or broader date range")

    rounded_trades_list = [round(num, 2) for num in trade_result]
    print(f'Trades List: {rounded_trades_list}')

    print(f'Dollar per Share profit2: ${round(sum(trade_result), 2)}')

    result = []
    for i in rounded_trades_list:
        if i > 0:
            result.append('profit')
        else:
            result.append('loss')

    print(result)
    trades_count = len(result)
    profitable_trades_count = result.count('profit')
    loss_trades_count = result.count('loss')
    win_percent = (profitable_trades_count * 100) / trades_count
    loss_percent = (loss_trades_count * 100) / trades_count

    print(f'Closed trades: {trades_count}')
    print(f'Profitable trades: {profitable_trades_count} ({round(win_percent, 2)}%)')
    print(f'Loss trades: {loss_trades_count} ({round(loss_percent, 2)}%)')


trades_analysis(trade_results_to_trade_analysis, trades_counter_to_trade_analysis)

#  ----------------------------------------------
#  PLOT CHART
#  ----------------------------------------------

#  Adding datetime column to dataframe
filtered_by_date_dataframe = (filtered_by_date_dataframe.assign(
    Datetime=(filtered_by_date_dataframe['Date'] + pd.to_timedelta(filtered_by_date_dataframe['Time']))))


def plot_line_chart(df):
    on_off = False   # To disable Line chart set to False

    if on_off:
        plt.figure(figsize=(15, 8))
        plt.plot(df['Datetime'], df['Close'], label='Ticker prices', marker='o')
        plt.title(f'{file_path}'.upper())
        plt.xlabel('Index')
        plt.ylabel('Price')
        plt.legend()


plot_line_chart(filtered_by_date_dataframe)


#  ----------------------------------------------
#  HIGHLIGHT SIGNALS
#  ----------------------------------------------


# date_time_dates = pd.to_datetime(filtered_by_date_dataframe['Datetime'])
# print('Date_time_dates: \n', date_time_dates)


def highlight_signal_on_chart(df):
    on_off = False   # To disable printing Line chart signals set to False

    if on_off:
        for i, s in enumerate(recognized_pattern):
            if s == 100:
                signal_date = df['Datetime'].iloc[i].strftime("%d-%m-%Y-%H-%M")
                annotation_text = f'Bullish signal on {signal_date} in {file_path}'
                # the point where the arrow will be pointing to:
                plt.annotate(annotation_text,
                             xy=(df['Datetime'].iloc[i], df['Close'].iloc[i]),
                             xytext=(df['Datetime'].iloc[i], df['Close'].iloc[i] + 100),
                             arrowprops=dict(arrowstyle='->')
                             )
            elif s == -100:
                signal_date = df['Datetime'].iloc[i].strftime("%d-%m-%Y-%H-%M")
                annotation_text = f'Bearish signal on {signal_date} {file_path}'
                # the point where the arrow will be pointing to:
                plt.annotate(annotation_text,
                             xy=(df['Datetime'].iloc[i], df['Close'].iloc[i]),
                             xytext=(df['Datetime'].iloc[i], df['Close'].iloc[i] + 100),
                             arrowprops=dict(arrowstyle='->')
                             )


highlight_signal_on_chart(filtered_by_date_dataframe)


def plot_candlestick_chart(df, signals):
    # warn_too_much_data = 200
    on_off = True

    if on_off:
        df.set_index('Datetime', inplace=True)

        add_plots = []  # Prepare additional plots
        # Add signals if provided
        # print(add_plots)
        # print(signals)

        signals_with_nan = signals.where(signals != 0, np.nan)  # replace values where the condition is False

        for i, s in enumerate(signals):     # Iterate over signals and add non-zero signals to add_plots
            if s != 0:
                # Add the signals as a subplot
                add_plots.append(mpf.make_addplot(signals_with_nan,
                                                  type='scatter', color='black', markersize=250, marker='+', panel=1))
                # Plot candlestick chart with additional plot
                # print(add_plots)
            else:
                pass
        print()
        print('Candlestick chart plotted')
        mpf.plot(df, type='candle', figsize=(15, 8), title=f'{file_path}'.upper(), ylabel='Price', addplot=add_plots,
                 warn_too_much_data=5000)


plot_candlestick_chart(filtered_by_date_dataframe, recognized_pattern)


plt.show()
