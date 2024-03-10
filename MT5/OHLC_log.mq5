//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
// We will use the static Old_Time variable to serve the bar time.
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
 
         // Print OHLC of the new bar
         double open = iOpen(_Symbol, _Period, 1); // Open price of the previous bar
         double high = iHigh(_Symbol, _Period, 1); // High price of the previous bar
         double low = iLow(_Symbol, _Period, 1); // Low price of the previous bar
         double close = iClose(_Symbol, _Period, 1); // Close price of the previous bar
         Print("Open: ", open, ", High: ", high, ", Low: ", low, ", Close: ", close);
         
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