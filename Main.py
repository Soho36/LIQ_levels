
from Pattern_rec import date_range_func

dataframe_source_api_or_csv = True    # True for API or response file, False for CSV
start_date = '2021-09-30'     # Choose the start date to begin from
end_date = '2022-07-21'     # Choose the end date
code_of_pattern = 50     # Choose the index of pattern (from Ta-lib patterns.csv)
risk_reward_ratio = 10   # Chose risk/reward ratio (how much you are aiming to win compared to lose)
stop_loss_as_candle_min_max = True  # Must be True if next condition is false

stop_loss_as_plus_candle = False     # Must be True if previous condition is false
stop_loss_offset_multiplier = 1    # 1 places stop one candle away from H/L (only when stop_loss_as_plus_candle = True
# ******************************************************************************

ticker_name, filtered_by_date_dataframe = date_range_func(start_date, end_date)