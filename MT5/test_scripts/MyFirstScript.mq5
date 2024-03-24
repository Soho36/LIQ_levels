//+------------------------------------------------------------------+
//|                                                MyFirstScript.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property script_show_inputs
input string name="";
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
Alert("Hello world!, "+name+"!");
Comment("Hello comment, "+name+"!");
   
  }
//+------------------------------------------------------------------+
