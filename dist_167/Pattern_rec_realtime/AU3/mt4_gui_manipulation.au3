
; Activate MetaTrader window
;WinActivate("44726481: ICMarketsSC-Demo04 - Demo Account - Raw Trading Ltd - [EURUSD,M1]")

; Send Alt+B shortcut to open new order window
;Send("!b")

; Wait for the new order window to become active
WinActivate("EURUSD, Euro vs US Dollar")
WinWaitActive("EURUSD, Euro vs US Dollar")

; Fill out form fields (replace placeholders with actual values)

;ControlSetText("New Order", "", "[CLASS:Edit; INSTANCE:2]", "Other form field value")

Sleep(3000)
;Set Volume
ControlFocus("EURUSD, Euro vs US Dollar", "", "[CLASS:Edit; INSTANCE:2]")
Sleep(1000)
ControlSend("EURUSD, Euro vs US Dollar", "", "[CLASS:Edit; INSTANCE:2]", "{LEFT}{LEFT}{LEFT}{LEFT}")
Sleep(1000)
Send("0.06")
Sleep(3000)
;ControlSetText("EURUSD, Euro vs US Dollar", "", "[CLASS:Edit; INSTANCE:2]", "0.05")
;Sleep(3000)

; Click Buy/Sell button
ControlClick("EURUSD, Euro vs US Dollar", "", "[CLASS:Button; TEXT:Buy]")	; BUY
;Sleep(2000)

;ControlClick("EURUSD, Euro vs US Dollar", "", "[CLASS:Button; TEXT:Sell]") ; SELL


;ControlClick("EURUSD, Euro vs US Dollar", "", "[CLASS:Button; TEXT:Close]")	; CLOSE

; Optionally, wait for the order to be executed
;WinWait("Order Confirmation", "", 10) ; Wait for 10 seconds for confirmation window

MsgBox(0, "Success", "Trade placed successfully!")
MsgBox(
