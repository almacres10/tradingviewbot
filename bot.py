import telebot
import yfinance as yf

API_KEY = '7123140191:AAEL-SOG_2Vtnnjn6gfDFSKyGVTYY5vlO2c'
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['Greet'])
def greet(message):
  bot.reply_to(message, "Hey! Hows it going?")

@bot.message_handler(commands=['hello'])
def hello(message):
  bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['wsb'])
def get_stocks(message):
  response = ""
  stocks = ['gme', 'amc', 'nok']
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='2d', interval='1d')
    data = data.reset_index()
    response += f"-----{stock}-----\n"
    stock_data.append([stock])
    columns = ['stock']
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'], 2)
      format_date = row['Date'].strftime('%m/%d')
      response += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()

  response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
  response += "\nStock Data"
  print(response)
  bot.send_message(message.chat.id, response)

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True

@bot.message_handler(func=stock_request)
def send_price(message):
    request = message.text.split()[1]
    data = yf.download(tickers=request, period='5d', interval='1d')

    if data.size > 0:
        data["format_date"] = data.index.strftime('%m/%d %I:%M %p')
        response = data[['Close', 'format_date']].to_string(header=False)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "No data!?")

# @bot.message_handler(func=stock_request)
# def send_price_minutely(message):
#     request = message.text.split()[1]
#     data = yf.download(tickers=request, period='5m', interval='1m')

#     if data.size > 0:
#         data["format_date"] = data.index.strftime('%m/%d %I:%M %p')
#         response = data[['Close', 'format_date']].to_string(header=False)
#         bot.send_message(message.chat.id, response)
#     else:
#         bot.send_message(message.chat.id, "No data!?")




bot.polling()