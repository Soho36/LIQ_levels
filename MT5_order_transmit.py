# import sys
import time
import subprocess

current_time = time.strftime('%H:%M:%S')
file_name = 'AU3/MT5_GUI_test.au3'

# ************************************** SETTINGS ***************************************
buy_or_sell_flag = False                                # True for "BUY", False for "SELL"
volume_value = 0.02                                    # 1000 MAX for stocks
stop_loss_value = 0
take_profit_value = 0
sleep = 500
# ***************************************************************************************

line_number_direction_buy_or_sell = 3
line_number_volume = 4
line_number_stop = 5
line_number_take = 6
line_number_sleep = 7
new_line_volume = f'Local $volume = {volume_value}' + '\n'
new_line_stop = f'Local $stop_loss = {stop_loss_value}' + '\n'
new_line_take = f'Local $take_profit = {take_profit_value}' + '\n'
new_line_direction_buy_or_sell = (f'Local $trade_direction_buy_or_sell = '
                                  f'{buy_or_sell_flag} ;True for BUY, False for Sell') + '\n'
new_line_sleep = f'Local $sleep = {sleep}' + '\n'


def order_send_func(filename):
    if buy_or_sell_flag:                                                # IF TRUE THEN "BUY", ELSE "SELL"
        with open(filename, 'r') as file:                               # Reading current au3.file
            lines = file.readlines()
            # print(lines)
        lines[line_number_volume - 1] = new_line_volume
        lines[line_number_stop - 1] = new_line_stop
        lines[line_number_take - 1] = new_line_take
        lines[line_number_direction_buy_or_sell - 1] = new_line_direction_buy_or_sell
        lines[line_number_sleep - 1] = new_line_sleep

        with open(filename, 'w') as file:                               # Writing au3.file with new lines
            file.writelines(lines)
    # SAME FOR "SELL"
    else:
        with open(filename, 'r') as file:                               # Reading current au3.file
            lines = file.readlines()
            # print(lines)
        lines[line_number_volume - 1] = new_line_volume
        lines[line_number_stop - 1] = new_line_stop
        lines[line_number_take - 1] = new_line_take
        lines[line_number_direction_buy_or_sell - 1] = new_line_direction_buy_or_sell
        lines[line_number_sleep - 1] = new_line_sleep

        with open(filename, 'w') as file:                               # Writing au3.file with new lines
            file.writelines(lines)

    print(f'File is saved at {current_time}')


order_send_func(file_name)

subprocess.run(['start', file_name], shell=True)                   # Run modified file through system shell
print(f'Order sent at {current_time}')
