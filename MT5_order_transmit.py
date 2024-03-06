import time
import subprocess

current_time = time.strftime('%H:%M:%S')
send_buy = True
send_sell = False
file_name = 'AU3/MT5_GUI.au3'
# write = 'AU3/MT5_GUI22.au3'
buy_order = 'buy'
sell_order = 'sell'

volume_value = 120  # 1000 MAX
stop_loss_value = 173.89
take_profit_value = 183.66

if send_buy:
    new_line_direction_buy = 3
elif send_sell:
    new_line_direction_sell = 4

line_number_volume = 5
line_number_stop = 6
line_number_take = 7
new_line_volume = f'Local $volume = {volume_value}' + '\n'
new_line_stop = f'Local $stop_loss = {stop_loss_value}' + '\n'
new_line_take = f'Local $take_profit = {take_profit_value}' + '\n'


def order_send(filename):
    if send_buy:
        with open(filename, 'r') as file:
            lines = file.readlines()
            print(lines)
        lines[line_number_volume - 1] = new_line_volume
        lines[line_number_stop - 1] = new_line_stop
        lines[line_number_take - 1] = new_line_take

        with open(filename, 'w') as file:
            file.writelines(lines)
    print(f'Filed is saved at {current_time}')


order_send(file_name)

subprocess.run(['start', file_name], shell=True)
print(f'Order sent at {current_time}')
