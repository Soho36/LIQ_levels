#define EXPERT_MAGIC 123456   // MagicNumber of the expert
//+------------------------------------------------------------------+
//| Opening Buy position                                             |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the trade request and result of trade request
   MqlTradeRequest request={};
   MqlTradeResult  result={};

//--- set ORDER parameters
   string ticker = "BTCUSD";
   string direction = "Buy";
   double vol = 0.01;
   double stop_loss_price = 64000;
   double take_profit_price = 70000;


//--- parameters of request
   request.action   =TRADE_ACTION_DEAL;                     // type of trade operation
   request.symbol   =ticker;                              // symbol
   request.volume   =vol;                                   // volume of 0.1 lot
   request.sl = stop_loss_price;                             // stop loss
   request.tp = take_profit_price;
   request.type     =ORDER_TYPE_BUY;                        // order type
   request.price    =SymbolInfoDouble(Symbol(),SYMBOL_ASK); // price for opening
   request.deviation=5;                                     // allowed deviation from the price
   request.magic    =EXPERT_MAGIC;                          // MagicNumber of the order


    

//--- send the request
   if(!OrderSend(request,result))
      PrintFormat("OrderSend error %d",GetLastError());     // if unable to send the request, output the error code
//--- information about the operation
   PrintFormat("retcode=%u  deal=%I64u  order=%I64u",result.retcode,result.deal,result.order);
  }
//+------------------------------------------------------------------+
