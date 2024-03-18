
; Activate MetaTrader window
WinActivate("44726481: ICMarketsSC-Demo04 - Demo Account - Raw Trading Ltd")

WinWaitActive("44726481: ICMarketsSC-Demo04 - Demo Account - Raw Trading Ltd")
;Send Alt+B shortcut to open new order window

Sleep(1000)
Send("{F9}")

;Activate Order Window
WinActivate("Order")
Sleep(1000)


;Set Volume
ControlFocus("Order", "", "[CLASS:Edit; INSTANCE:10]")
Sleep(1000)
ControlSend("Order", "", "[CLASS:Edit; INSTANCE:10]", "{BACKSPACE}")
Sleep(1000)
Send("0.05")
Sleep(1000)

;Set Stop Loss
ControlFocus("Order", "", "[CLASS:Edit; INSTANCE:11]")
Sleep(1000)
ControlSend("Order", "", "[CLASS:Edit; INSTANCE:11]", "{BACKSPACE}")
Sleep(1000)
Send("1.06")
Sleep(1000)

;Set Take Profit
ControlFocus("Order", "", "[CLASS:Edit; INSTANCE:12]")
Sleep(1000)
ControlSend("Order", "", "[CLASS:Edit; INSTANCE:12]", "{BACKSPACE}")
Sleep(1000)
Send("1.1")
Sleep(1000)


; Click Buy/Sell button
ControlClick("Order", "", "[CLASS:Button; TEXT:Buy by Market]")	; BUY
;MsgBox(0, "Trade opened", "Trade placed successfully!")

Sleep(2000)
Send("{F9}")

;Sleep(5000)
;Send("!b")
;WinActivate("EURUSD, Euro vs US Dollar")
;WinWaitActive("EURUSD, Euro vs US Dollar")
;Sleep(1000)
;ControlClick("EURUSD, Euro vs US Dollar", "", "[CLASS:Button; INSTANCE:2]")	; CLOSE
;Sleep(1000)
;MsgBox(0, "Trade is closed", "Trade closed successfully!")


