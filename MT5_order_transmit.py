import sys
import time
import subprocess

current_time = time.strftime('%H:%M:%S')
file_name = 'AU3/MT5_GUI.au3'

# ************************************** SETTINGS ***************************************
send_buy = False
send_sell = True
volume_value = 100  # 1000 MAX
stop_loss_value = 179.25
take_profit_value = 178.75
# ***************************************************************************************

line_number_direction_buy = 3
line_number_direction_sell = 4
line_number_volume = 5
line_number_stop = 6
line_number_take = 7
new_line_volume = f'Local $volume = {volume_value}' + '\n'
new_line_stop = f'Local $stop_loss = {stop_loss_value}' + '\n'
new_line_take = f'Local $take_profit = {take_profit_value}' + '\n'
new_line_direction_buy = f'Local $trade_direction_buy = {send_buy}' + '\n'
new_line_direction_sell = f'Local $trade_direction_sell = {send_sell}' + '\n'


def order_send(filename):
    if send_buy and send_sell:
        print("Only one condition can be True - Buy or Sell")
        sys.exit()
    if send_buy:
        with open(filename, 'r') as file:   # Reading current au3.file
            lines = file.readlines()
            print(lines)
        lines[line_number_volume - 1] = new_line_volume
        lines[line_number_stop - 1] = new_line_stop
        lines[line_number_take - 1] = new_line_take
        lines[line_number_direction_buy - 1] = new_line_direction_buy
        lines[line_number_direction_sell - 1] = new_line_direction_sell

        with open(filename, 'w') as file:   # Writing au3.file with new lines
            file.writelines(lines)

    if send_sell:
        with open(filename, 'r') as file:   # Reading current au3.file
            lines = file.readlines()
            # print(lines)
        lines[line_number_volume - 1] = new_line_volume
        lines[line_number_stop - 1] = new_line_stop
        lines[line_number_take - 1] = new_line_take
        lines[line_number_direction_buy - 1] = new_line_direction_buy
        lines[line_number_direction_sell - 1] = new_line_direction_sell

        with open(filename, 'w') as file:   # Writing au3.file with new lines
            file.writelines(lines)
    else:
        pass
    print(f'File is saved at {current_time}')


order_send(file_name)

subprocess.run(['start', file_name], shell=True)    # Run modified file through system shell
print(f'Order sent at {current_time}')
