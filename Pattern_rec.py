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
file_path = 'TXT/tsla_D1.csv'
# file_path = 'TXT/neog_D1.csv'
# file_path = 'TXT/meta_D1.csv'
# file_path = 'TXT/tsla_m5.csv'
# file_path = 'TXT/tsla_m1.csv'
# file_path = 'TXT/MT4/BTCUSD_D1.csv'
# file_path = 'TXT/MT4/BTCUSD_m60.csv'
# file_path = 'TXT/MT4/BTCUSD_m5.csv'
# ------------------------------------------
# pd.set_option('display.max_columns', 10)  # Uncomment to display all columns


# ******************************************************************************
start_date = '2023-04-06'     # Choose the start date to begin from
end_date = '2023-05-20'     # Choose the end date
code_of_pattern = 18     # Choose the index of pattern (from Ta-lib patterns.csv)
# ******************************************************************************


def getting_dataframe_from_file(path):

    directory_path = 'TXT/'
    print('\nDatafiles in folder: ')
    for filename in os.listdir(directory_path):     # Making a list of files located in TXT folder
        print(filename)

    print('\nCurrent file is: ', path)

    columns_to_parce = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Filename']

    #  for MT4 files set dayfirst=False
    csv_df = pd.read_csv(path, parse_dates=[0], dayfirst=False, usecols=columns_to_parce)
    print('\nDataframe derived from CSV: \n', csv_df.head())
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
print('\nFiltered by date dataframe: \n', filtered_by_date_dataframe.head())


#  ----------------------------------------------
#  PATTERN RECOGNITION
#  ----------------------------------------------

patterns_dataframe = pd.read_csv('Ta-lib patterns.csv')


def pattern_recognition_func(patterns_df, code):  # Reading Pattern codes from CSV

    pattern_code = patterns_df['PatternCode'].iloc[code]
    pattern_name = patterns_df['PatternName'].iloc[code]
    pattern_index = patterns_df.index[code]
    print('\nCurrent Pattern is: ', pattern_code, ',', pattern_name, ', ', pattern_index)

    pattern_function = getattr(talib, pattern_code)
    signal = pattern_function(filtered_by_date_dataframe['Open'], filtered_by_date_dataframe['High'],
                              filtered_by_date_dataframe['Low'], filtered_by_date_dataframe['Close'])

    return signal


recognized_pattern = pattern_recognition_func(patterns_dataframe, code_of_pattern)  # Returns series
# print(recognized_pattern)


#  ----------------------------------------------
#  TRADES SIMULATION
#  ----------------------------------------------


def trades_simulation(filtered_df):
    on_off = True
    if on_off:
        counter = 0
        for signal_index, signal_value in enumerate(recognized_pattern):

            # LONG TRADES LOGIC
            if signal_value == 100:
                counter += 1
                date = filtered_df.iloc[signal_index]['Date']
                candle_close_entry = round(filtered_df.iloc[signal_index]['Close'], 2)
                low = round(filtered_df.iloc[signal_index]['Low'], 2)
                stop_loss_price = low
                take_profit_price = round((candle_close_entry - low) * 2) + candle_close_entry
                print('\nOpen long trade: '.upper(), date,
                      '| Entry price:', candle_close_entry,
                      '  Stop:', stop_loss_price,
                      '  Take:', take_profit_price)
                print()
                for j in range(signal_index + 1, len(filtered_df)):
                    current_candle_date = filtered_df.iloc[j]['Date']
                    current_candle_open = filtered_df.iloc[j]['Open']
                    current_candle_high = filtered_df.iloc[j]['High']
                    current_candle_low = filtered_df.iloc[j]['Low']
                    current_candle_close = filtered_df.iloc[j]['Close']

                    print('Current candle OHLC: ', current_candle_date, '|',
                          'O', current_candle_open,
                          'H', current_candle_high,
                          'L', current_candle_low,
                          'C', current_candle_close)
                    if current_candle_high >= take_profit_price:
                        print(f'Take profit hit at {take_profit_price}')
                        break
                    elif current_candle_low <= stop_loss_price:
                        print(f'Stop Loss hit at {stop_loss_price}')
                        break
                    else:
                        pass
                        # print('Still Open')

            # SHORT TRADES LOGIC
            elif signal_value == -100:
                counter += 1
                date = filtered_df.iloc[signal_index]['Date']
                candle_close_entry = round(filtered_df.iloc[signal_index]['Close'], 2)
                high = round(filtered_df.iloc[signal_index]['High'], 2)
                stop_loss_price = high
                take_profit_price = candle_close_entry - round((high - candle_close_entry) * 2)
                print('\nOpen short trade: '.upper(), date,
                      '| Entry price:', candle_close_entry,
                      '  Stop:', stop_loss_price,
                      '  Take:', take_profit_price)
                print()
                for j in range(signal_index + 1, len(filtered_df)):
                    current_candle_date = filtered_df.iloc[j]['Date']
                    current_candle_open = filtered_df.iloc[j]['Open']
                    current_candle_high = filtered_df.iloc[j]['High']
                    current_candle_low = filtered_df.iloc[j]['Low']
                    current_candle_close = filtered_df.iloc[j]['Close']

                    print('Current candle OHLC: ', current_candle_date, '|',
                          'O', current_candle_open,
                          'H', current_candle_high,
                          'L', current_candle_low,
                          'C', current_candle_close)
                    if current_candle_low <= take_profit_price:
                        print(f'Take profit hit at {take_profit_price}')
                        break
                    elif current_candle_high >= stop_loss_price:
                        print(f'Stop Loss hit at {stop_loss_price}')
                        break
                    else:
                        pass
                        # print('Still Open')

        print('Executed trades: ', counter)

        if counter == 0:
            print("No trades were placed! Try other pattern or broader date range")


trades_simulation(filtered_by_date_dataframe)


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
        print('\nCandlestick chart plotted')
        mpf.plot(df, type='candle', figsize=(15, 8), title=f'{file_path}'.upper(), ylabel='Price', addplot=add_plots,
                 warn_too_much_data=5000)


plot_candlestick_chart(filtered_by_date_dataframe, recognized_pattern)


plt.show()
