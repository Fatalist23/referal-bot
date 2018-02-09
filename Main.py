import telebot
import pymysql.cursors
import httplib2
import apiclient.discovery

from oauth2client.service_account import ServiceAccountCredentials
from telebot import types
#TeleLogin
TOKEN = '544371953:AAFeIgyJPh8gxe5VgBRKHXG7ZedWNbNHUIY'
bot= telebot.TeleBot(TOKEN)
#DB Login
connect = pymysql.connect(host='127.0.0.1',
                          user='admin',
                          password='230298',
                          db='userdb',
                          )
print ("Connect successful!")

updates = bot.get_updates()

MainMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
MainBtn = types.KeyboardButton("Нажми на кнопку")
MainMarkup.add(MainBtn)

userid=0
@bot.message_handler(commands=['start'])
def startmessage(message):
    bot.send_message(message.chat.id,text='Нажми на кнопку',reply_markup=MainMarkup)

def Check(id):

@bot.message_handler(content_types=['text'])
def allmessages(message):
    bot.send_message(message.chat.id,text='sad',reply_markup=MainMarkup)

bot.polling(none_stop=True)