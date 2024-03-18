; Specify the path to the file you want to open
Local $filePath = "E:\YandexDisk\Desktop_Zal\2022ID.jpg"

; Check if the file exists
If FileExists($filePath) Then
    ; Open the file using the default associated program
    ShellExecute($filePath)
    MsgBox(0, "Success", "File opened successfully")
Else
    MsgBox(16, "Error", "File not found: " & $filePath)
EndIf
