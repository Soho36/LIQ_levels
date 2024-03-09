# Copyright 2024, MetaQuotes Ltd.
# https://www.mql5.com

import MetaTrader5 as mt5

mt5.initialize()

# Open the file for writing
file_handle = open("CandleLog.csv", "a")

# Main loop to continuously monitor for new candles
while True:
    # Get the latest candle information
    latest_candle = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M1, 0, 1)[0]

    # Extract OHLC data from the candle
    open_price = latest_candle.open
    high_price = latest_candle.high
    low_price = latest_candle.low
    close_price = latest_candle.close

    # Write OHLC data to the log file
    file_handle.write(f"{latest_candle.time},{open_price},{high_price},{low_price},{close_price}\n")
    file_handle.flush()  # Ensure data is written to file immediately

    # Sleep for a short duration before checking for the next candle
    mt5.sleep(1000)  # Sleep for 1 second (adjust as needed)

# Close the file and shutdown MetaTrader 5 connection
file_handle.close()
mt5.shutdown()
