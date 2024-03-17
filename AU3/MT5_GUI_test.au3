;IF LINES ARE ADDED OR REMOVED WITHIN THIS BLOCK CORRESPONDING INDEXES MUST BE UPDATED IN PYTHON SCRIPT
; ALL VALUES DERIVED FROM PYTHON SCRIPT
Local $trade_direction_buy_or_sell = True ;replaceable line. True for BUY, False for Sell
Local $volume = 0.01 ;replaceable line
Local $stop_loss = 67083.35 ;replaceable line
Local $take_profit = 67232.55 ;replaceable line
Local $sleep = 200 ;replaceable line

;IF LINES ARE ADDED OR REMOVED WITHIN THIS BLOCK CORRESPONDING INDEXES MUST BE UPDATED IN PYTHON SCRIPT
;************************************************************************************************************
; Activate MetaTrader window
WinActivate("19079167")

WinWaitActive("19079167")
;Send Alt+B shortcut to open new order window

Sleep($sleep)
Send("{F9}")

;Activate Order Window
WinActivate("Order")
Sleep($sleep)

;Set Volume
;ControlFocus("Order", "", "[CLASS:Edit; INSTANCE:25]")
;Sleep($sleep)
;ControlSend("Order", "", "[CLASS:Edit; INSTANCE:25]", "{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}")
;Sleep($sleep)
;Send($volume)
;Sleep($sleep)

;Set Volume2
Send("{TAB}{TAB}{BACKSPACE}")
Send($volume)
;Sleep($sleep)

;Set Stop Loss for BUY order2
Send("{TAB}{BACKSPACE}")
Send($stop_loss)
;Sleep($sleep)

;Set Take Profit for BUY order2
Send("{TAB}{BACKSPACE}")
Send($take_profit)
;Sleep($sleep)

;Set Stop Loss for BUY order
;ControlFocus("Order", "", "[CLASS:Edit; INSTANCE:26]")
;Sleep($sleep)
;ControlSend("Order", "", "[CLASS:Edit; INSTANCE:26]", "{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}")
;Sleep($sleep)
;Send($stop_loss)
;Sleep($sleep)

;Set Take Profit for BUY order
;ControlFocus("Order", "", "[CLASS:Edit; INSTANCE:28]")
;Sleep($sleep)
;ControlSend("Order", "", "[CLASS:Edit; INSTANCE:28]", "{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{RIGHT}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}")
;Sleep($sleep)
;Send($take_profit)
;Sleep($sleep)

;Set Take Profit for BUY order2



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

; Reactivate order window to faster access
Sleep($sleep)
Send("{F9}")








