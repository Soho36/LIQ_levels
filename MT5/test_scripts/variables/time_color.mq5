//+------------------------------------------------------------------+
//|                                                           33.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property script_show_inputs
//--- input parameters
input bool     Input1=false;
input int      Input2=3;
input double   Input3=4.2;
input string   Input4="";
input color    Input5=clrLightCyan;
input datetime Input6=D'2024.03.20 00:13:22';
datetime time=0;
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
Print(int(Input5)," ", int(Input6));
Print(time);
time+=86400;
Print(time);

    
  }
//+------------------------------------------------------------------+
