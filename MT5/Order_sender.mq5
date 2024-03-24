//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
// Will use the static Old_Time variable to serve the bar time.
// At each OnTick execution we will check the current bar time with the saved one.
// If the bar time isn't equal to the saved time, it indicates that we have a new tick.
   static datetime Old_Time;
   datetime New_Time[1];
   bool IsNewBar=false;

// copying the last bar time to the element New_Time[0]
   int copied=CopyTime(_Symbol,_Period,0,1,New_Time);
   if(copied>0) // ok, the data has been copied successfully
     {
      if(Old_Time!=New_Time[0]) // if old time isn't equal to new bar time
        {
         IsNewBar=true;   // if it isn't a first call, the new bar has appeared
 
         // Start of main logic
         #define EXPERT_MAGIC 123456   // MagicNumber of the expert

         {
             string fileName = "buy_sell_signals_from_python.txt";
         
             // Check if the file exists
             if (!FileIsExist(fileName))
             {
                 Print("File does not exist: ", fileName);
                 return;
             }
             
             Sleep(3000);
             
         //+------------------------------------------------------------------+
         //| Opening file for reading                                         |
         //+------------------------------------------------------------------+
         
             {
                 // Open the file for reading
                 int fileHandle = FileOpen(fileName, FILE_READ|FILE_ANSI);
                 if (fileHandle == INVALID_HANDLE)
                 {
                     Print("Failed to open file: ", GetLastError());
                     return;
                 }
                 
                 // Read the entire contents of the file
                 ulong fileSize = FileSize(fileHandle);
                 if (fileSize > 0)
                 {
                     string signal = FileReadString(fileHandle, fileSize);
                     
                     // Clear the contents of the file
                     
                     FileClose(fileHandle);                                   // Close the file before writing to it
                     
                     fileHandle = FileOpen(fileName, FILE_WRITE | FILE_ANSI); // Reopen the file in write mode
                     if (fileHandle != INVALID_HANDLE)
                     {
                        FileWriteString(fileHandle, "");                      // Write an empty string to clear the file
                        FileClose(fileHandle);                                // Close the file after clearing it
                     }
                     else
                     {
                        Print("Failed to open file for writing: ", GetLastError());
                     }
                     
                     Print(signal);                                           //Print file contents
                     
                     // Split the signal into components
                     string components[];
                     int count = StringSplit(signal, ',', components);
                     if (count >= 2)
                     {
                         string symbol = components[0]; // Symbol (e.g., "BTCUSD")
                         string direction = components[1]; // Direction (e.g., "Buy")
                         double stop_loss = StringToDouble(components[2]);  // Stop-Loss
                         double take_profit = StringToDouble(components[3]); // Take profit
                         double volume = 0.01;
                         Print(symbol," ", direction," ", stop_loss," ", take_profit);           //Print received data
                                                
         //+------------------------------------------------------------------+
         //| Opening Buy position                                             |
         //+------------------------------------------------------------------+
                         
                         if (direction == "Buy")
                         {
                             // Declare and initialize the trade request and result of trade request
                             MqlTradeRequest request = {};
                             MqlTradeResult result = {};
         
                             // Parameters of request
                             request.action = TRADE_ACTION_DEAL;                                   // Type of trade operation
                             request.symbol = symbol; // Symbol
                             request.volume = volume;
                             request.sl = stop_loss;
                             request.tp = take_profit;
                             request.type = ORDER_TYPE_BUY; // Order type
                             request.price = SymbolInfoDouble(Symbol(), SYMBOL_ASK);               // Price for opening
                             request.deviation = 5; // Allowed deviation from the price
                             request.magic = EXPERT_MAGIC; // MagicNumber of the order
                             request.comment = "250324";
                             
                             // Send the request
                             if (!OrderSend(request, result))
                             {
                                 Print("OrderSend error ", GetLastError()); // If unable to send the request, output the error code
                             }
                             else
                             {
                                 // Information about the operation
                                 PrintFormat("retcode=%u  deal=%I64u  order=%I64u", result.retcode, result.deal, result.order);
                             }
                         }
         
         //+------------------------------------------------------------------+
         //| Opening Sell position                                            |
         //+------------------------------------------------------------------+                                
                         
                         if (direction == "Sell")
                         {
                              // Declare and initialize the trade request and result of trade request
                             MqlTradeRequest request = {};
                             MqlTradeResult result = {};
         
                             // Parameters of request
                             request.action = TRADE_ACTION_DEAL; // Type of trade operation
                             request.symbol = symbol; // Symbol
                             request.volume = volume; 
                             request.sl = stop_loss;
                             request.tp = take_profit;
                             request.type = ORDER_TYPE_SELL; // Order type
                             request.price = SymbolInfoDouble(Symbol(), SYMBOL_ASK); // Price for opening
                             request.deviation = 5; // Allowed deviation from the price
                             request.magic = EXPERT_MAGIC; // MagicNumber of the order
                             request.comment = "250324";
                             
                             // Send the request
                             if (!OrderSend(request, result))
                             {
                                 Print("OrderSend error ", GetLastError()); // If unable to send the request, output the error code
                             }
                             else
                             {
                                 // Information about the operation
                                 PrintFormat("retcode=%u  deal=%I64u  order=%I64u", result.retcode, result.deal, result.order);
                             }
                         }
                         
                     }
                 }
                 else
                 {
                     FileClose(fileHandle);
                 }
                 
                 // Sleep(1000); // Sleep for 1 second before checking again
             }
         }

         
         // End of main logic
         
         Old_Time=New_Time[0];            // saving bar time
        }
     }
   else
     {
      Alert("Error in copying historical times data, error =",GetLastError());
      ResetLastError();
      return;
     }

//--- EA should only check for new trade if we have a new bar
   if(IsNewBar==false)
     {
      return;
     }
  }