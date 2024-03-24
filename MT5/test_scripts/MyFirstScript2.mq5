//+------------------------------------------------------------------+
//|                                                MyFirstScript.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property script_show_inputs
input string name="";
string _name;
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
_name=name;
StringTrimLeft(_name);
StringTrimRight(_name);
if(_name==""){
Alert("You must enter a name");
return;
}
Alert("Hello, "+_name+"!");   
  }
//+------------------------------------------------------------------+
