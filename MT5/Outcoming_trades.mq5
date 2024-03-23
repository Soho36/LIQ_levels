#define EXPERT_MAGIC 123456   // MagicNumber of the expert

void OnStart()
{
    string fileName = "buy_sell_signals_for_mt5.txt";

    // Check if the file exists
    if (!FileIsExist(fileName))
    {
        Print("File does not exist: ", fileName);
        return;
    }
    
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
            FileClose(fileHandle);
            Print(signal);                                                             //Print file contents
            
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
                
                else
                {
                     Print("Wrong file contents");
                }
            }
        }
        else
        {
            FileClose(fileHandle);
        }
        
        Sleep(1000); // Sleep for 1 second before checking again
    }
}
