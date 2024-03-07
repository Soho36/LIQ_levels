;IF LINES ARE ADDED OR REMOVED WITHIN THIS BLOCK CORRESPONDING INDEXES MUST BE UPDATED IN PYTHON SCRIPT
; ALL VALUES DERIVED FROM PYTHON SCRIPT
Local $trade_direction_buy = False
Local $trade_direction_sell = True
Local $volume = 100
Local $stop_loss = 179.25
Local $take_profit = 178.75
Local $sleep = 1000

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
If $trade_direction_buy Then
	ControlClick("Order", "", "[CLASS:Button; INSTANCE:20]")	; BUY
ElseIf $trade_direction_sell Then
	ControlClick("Order", "", "[CLASS:Button; INSTANCE:19]")	; SELL
EndIf



