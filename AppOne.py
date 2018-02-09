from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import mysql.connector
import telebot
from telebot import types
#Telega
TOKEN = '546132218:AAGvBSF7dI0QTxKLvwLFlKD0aaFXYBp2_Nc'
bot= telebot.TeleBot(TOKEN)
#БД
dbconfig = { 'host': '127.0.0.1',
             'user': 'seregatest',
             'password': 'seregatestpass',
             'database': 'testbase', }

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor(buffered=True)
#Клавиатура
MainMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
MainBtn = types.KeyboardButton("Нажми на кнопку")
MainMarkup.add(MainBtn)

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
def searchuser (usID):
    usercounter = -1
    cursor.execute("SELECT refCount FROM users WHERE userID =" + str(usID))
    res = cursor.fetchall()
    if (res != []):
        usercounter = res[0][0]
    return usercounter


def ifrefed (usID):
    wasrefed = False
    cursor.execute("SELECT ifInv FROM users WHERE userID =" + str(usID))
    res = cursor.fetchall()
    if ((res[0][0])==1):
        wasrefed = True
    return wasrefed


def adduser (usID, refID):
    uscounter = searchuser(usID)
    refcounter = searchuser(refID)
    if (refID == 0):
        if (uscounter==-1):
            cursor.execute("INSERT INTO users VALUES (%s,%s,%s)", (usID, 0, 0))
            conn.commit()
            return (uscounter)
        else:
            return (uscounter)
    else:
        if (refcounter == -1):
            if (uscounter == -1):
                cursor.execute("INSERT INTO users VALUES (%s,%s,%s)", (usID, 0, 0))
                conn.commit()
                return (uscounter)
            else:
                return (uscounter)
        else:
            if (uscounter == -1):
                if (ifrefed(usID)==False):
                    refcounter = refcounter +1
                    cursor.execute("UPDATE `users` SET refCounter=" + str(refcounter) + " WHERE `usserID` =" + str(usID))
                    cursor.execute("INSERT INTO users VALUES (%s,%s,%s)", (usID, 0, 1))
                    conn.commit()
                    return uscounter
                else:
                    cursor.execute("INSERT INTO users VALUES (%s,%s,%s)", (usID, 0, 1))
                    conn.commit()
                    return uscounter
            else:
                if (ifrefed(usID)==False):
                    refcounter = refcounter +1
                    cursor.execute("UPDATE `users` SET refCounter=" + str(refcounter) + " WHERE `usserID` =" + str(usID))
                    return uscounter
                else:
                    return uscounter


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message ( message.chat.id , text='Подписаться на уведомления' , reply_markup=MainMarkup )
    Refer_ID = message.text[6:]
    User_ID= message.chat.id
    for s in Refer_ID:
        if isint(s)==False:
            letter = True
        else:
            letter = False
    if letter == False:
        adduser(User_ID,Refer_ID)
    else:
        adduser(User_ID,0)


bot.polling(none_stop=True)