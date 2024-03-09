//+------------------------------------------------------------------+
//|                                               OHLC_Logger.mq5    |
//|                        Copyright 2024, MetaQuotes Ltd.           |
//|                                              https://www.mql5.com|
//+------------------------------------------------------------------+
#property strict

#include <Trade\Trade.mqh> // Include for trading functions
#include <ChartObjects\ChartObject.mqh> // Include for object functions

// File handle
int fileHandle;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    // Open the file for writing
    fileHandle = FileOpen("OHLC_Log.csv", FILE_WRITE|FILE_TXT|FILE_CSV);
    if(fileHandle == INVALID_HANDLE)
    {
        Print("Failed to open file for writing! Error code: ", GetLastError());
        return INIT_FAILED;
    }
    
    // Set timer to check for completed candles every second
    EventSetTimer(1);
    
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    // Close the file
    FileClose(fileHandle);
    
    // Reset timer
    EventKillTimer();
}

//+------------------------------------------------------------------+
//| Expert timer function                                           |
//+------------------------------------------------------------------+
// Declare a boolean variable to keep track of whether the condition is met
bool conditionMet = false;

void OnTimer()
{
    // Get the opening time of the last completed candle
    datetime previousCandleTime = iTime(Symbol(), Period(), 1);

    // Get the current time
    datetime currentTime = TimeCurrent();

    MqlDateTime currentCandle, previousCandle;
    TimeToStruct(currentTime, currentCandle);
    TimeToStruct(previousCandleTime, previousCandle);

    // Check if a new candle has formed and the condition is met
    if (currentCandle.min % 5 == 0 && currentCandle.min != previousCandle.min && !conditionMet)
    {
        // Print a debug message to verify the conditions are met
        Print("Current Time: ", TimeToString(currentTime, TIME_DATE | TIME_MINUTES));
        Print("Previous Candle Time: ", TimeToString(previousCandleTime, TIME_DATE | TIME_MINUTES));

        // Get the closed candle OHLC data
        double openPrice = iOpen(Symbol(), Period(), 1);
        double highPrice = iHigh(Symbol(), Period(), 1);
        double lowPrice = iLow(Symbol(), Period(), 1);
        double closePrice = iClose(Symbol(), Period(), 1);
        datetime candleTime = previousCandleTime; // Time of the completed candle

        // Format the data
        string dataRow = TimeToString(candleTime, TIME_DATE) + "," +
                         TimeToString(candleTime, TIME_MINUTES) + "," +
                         DoubleToString(openPrice, _Digits) + "," +
                         DoubleToString(highPrice, _Digits) + "," +
                         DoubleToString(lowPrice, _Digits) + "," +
                         DoubleToString(closePrice, _Digits);

        // Write data row to the log file
        FileWriteString(fileHandle, dataRow + "\n");
        
        // Set the conditionMet variable to true
        conditionMet = true;
    }
    
    // Reset conditionMet if the condition is no longer met
    if (currentCandle.min % 5 != 0 || currentCandle.min == previousCandle.min)
    {
        conditionMet = false;
    }
}
