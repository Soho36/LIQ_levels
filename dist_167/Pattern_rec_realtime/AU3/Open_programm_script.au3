; Specify the path to the program executable
Local $programPath = "E:\YandexDisk\Desktop_Zal\2022ID.jpg"

; Check if the program executable exists
If FileExists($programPath) Then
    ; Open the program
    Run($programPath)
    ; Optional: Add a delay to ensure the program has enough time to open
    Sleep(2000) ; Sleep for 2 seconds (adjust as needed)
    MsgBox(0, "Success", "Program opened successfully")
Else
    MsgBox(16, "Error", "Program executable not found: " & $programPath)
EndIf
