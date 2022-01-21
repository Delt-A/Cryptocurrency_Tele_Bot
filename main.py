import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

CMC_API = os.environ['CMC_API']
API_KEY = os.environ['API_KEY']
updater = Updater(API_KEY,
				use_context=True)


def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Enter the text you want to show to the user whenever they start the bot")



#code chính nằm ở đây:
def price( update: Update, context: CallbackContext):
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
  parameters = {
    'symbol': 'nfty',
    'convert':'USD'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CMC_API,
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)['data']['NFTY']['quote']['USD']['price']
    update.message.reply_text(data)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
    update.message.reply_text(e)




###############################################


def help(update: Update, context: CallbackContext):
	update.message.reply_text("Your Message")



def default(update: Update, context: CallbackContext):
	update.message.reply_text("")

def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry I can't recognize you , you said '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('price', price))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
	# Filters out unknown commands
	Filters.command, unknown))

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
updater.start_polling()
