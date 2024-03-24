//+------------------------------------------------------------------+
//|                                                    increment.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
int i=4, j=7;
double t=43.78;
int k=0;
int digits=2;

//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {

k=i+(++j);
Print(i);
Print(j);
Print(k);
Print("Max value: ", MathMax(i, j));
Print("Rounded: ", round(t));
Print("Rounded to a given numer of digits: ", NormalizeDouble(t, digits));
Print("Random number: ", MathRand());
Print("Server time: ", TimeCurrent());


   
  }
//+------------------------------------------------------------------+
