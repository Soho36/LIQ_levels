;IF LINES ARE ADDED OR REMOVED WITHIN THIS BLOCK CORRESPONDING INDEXES MUST BE UPDATED IN PYTHON SCRIPT
; ALL VALUES DERIVED FROM PYTHON SCRIPT
Local $trade_direction_buy_or_sell = False ;replaceable line. True for BUY, False for Sell
Local $volume = 0.01 ;replaceable line
Local $stop_loss = 68125.41 ;replaceable line
Local $take_profit = 68116.21 ;replaceable line
Local $sleep = 200 ;replaceable line

;IF LINES ARE ADDED OR REMOVED WITHIN THIS BLOCK CORRESPONDING INDEXES MUST BE UPDATED IN PYTHON SCRIPT
;************************************************************************************************************
; Activate MetaTrader window
WinActivate("51679144")

WinWaitActive("51679144")
;Send Alt+B shortcut to open new order window

Sleep($sleep)
Send("{F9}")

;Activate Order Window
WinActivate("Order")
Sleep($sleep)

;Set Volume
ControlFocus("Order", "", "[CLASS:Edit; INSTANCE:25]")
Sleep($sleep)
ControlSend("Order", "", "[CLASS:Edit; INSTANCE:25]", "{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}")
Sleep($sleep)
Send($volume)
Sleep($sleep)

;Set Stop Loss for BUY order
ControlFocus("Order", "", "[CLASS:Edit; INSTANCE:26]")
Sleep($sleep)
ControlSend("Order", "", "[CLASS:Edit; INSTANCE:26]", "{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}")
Sleep($sleep)
Send($stop_loss)
Sleep($sleep)

;Set Take Profit for BUY order
ControlFocus("Order", "", "[CLASS:Edit; INSTANCE:28]")
Sleep($sleep)
ControlSend("Order", "", "[CLASS:Edit; INSTANCE:28]", "{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}")
Sleep($sleep)
Send($take_profit)
Sleep($sleep)

; Click Buy/Sell button
If $trade_direction_buy_or_sell Then
	ControlClick("Order", "", "[CLASS:Button; INSTANCE:20]")	; BUY
Else
	ControlClick("Order", "", "[CLASS:Button; INSTANCE:19]")	; SELL
EndIf

Sleep($sleep)

;Activate Order Window if ERROR
WinActivate("Order")
Sleep($sleep)

; Click Buy/Sell button
WinClose("Order")







