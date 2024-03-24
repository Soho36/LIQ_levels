//+------------------------------------------------------------------+
//|                                                     overflow.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"

//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
double z=1.2345/10;
Print(DoubleToString(z, 16));
Print(NormalizeDouble(z, 3));


  }
//+------------------------------------------------------------------+
