# Open the file in read mode
with open('C:/Users/Vova deduskin lap/AppData/Roaming/MetaQuotes/Terminal/010E047102812FC0C18890992854220E'
          '/MQL5/Logs/20240310.log', 'r', encoding='utf-16') as file:
# with open('C:/Users/Vova deduskin lap/AppData/Roaming/MetaQuotes/Terminal/010E047102812FC0C18890992854220E'
#           '/MQL5/Files/OHLC_Log.csv', 'r', encoding='utf-16') as file:

    data = file.read()
print(data)