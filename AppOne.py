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
MainBtn = types.KeyboardButton("Ты")
MainMarkup.add(MainBtn)
MainBtn1 = types.KeyboardButton("Пидор")
MainMarkup.add(MainBtn1)


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
    if (res!=[]):
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
            uscounter = 0
            print("tut4")
            return (uscounter)
        else:
            print("tut8")
            return (uscounter)
    else:
        if (refcounter == -1):
            if (uscounter == -1):
                cursor.execute("INSERT INTO users VALUES (%s,%s,%s)", (usID, 0, 0))
                conn.commit()
                uscounter = 0
                print("tut3")
                return (uscounter)
            else:
                print("tut7")
                return (uscounter)
        else:
            if (uscounter == -1):
                if (ifrefed(usID)==False):
                    if (usID == refID):
                        cursor.execute("INSERT INTO users VALUES (%s,%s,%s)", (usID, 0, 0))
                        conn.commit()
                        uscounter = 0
                        print("tut2")
                        return (uscounter)
                    else:
                        refcounter = refcounter +1
                        cursor.execute("UPDATE `users` SET refCount=" + str(refcounter) + " WHERE `userID` =" + str(usID))
                        conn.commit()
                        cursor.execute("INSERT INTO users VALUES (%s,%s,%s)", (usID, 0, 1))
                        conn.commit()
                        uscounter = 0
                        print("tut1")
                        return uscounter
                else:
                    cursor.execute("INSERT INTO users VALUES (%s,%s,%s)", (usID, 0, 1))
                    conn.commit()
                    print("tut")
                    return uscounter
            else:
                if (ifrefed(usID)==False):
                    if (usID == refID):
                        print("tut11")
                        return uscounter
                    else:
                        refcounter = refcounter +1
                        cursor.execute("UPDATE `users` SET refCount=" + str(refcounter) + " WHERE `userID` =" + str(refID))
                        conn.commit()
                        cursor.execute("UPDATE `users` SET ifInv=1"+ " WHERE `userID` =" + str(usID))
                        conn.commit()
                        return uscounter
                else:
                    print("tut5")
                    return uscounter


@bot.message_handler(commands=['start'])
def start(message):
    Refer_ID = message.text[6:]
    User_ID= message.chat.id
    print (Refer_ID)
    print (User_ID)

    found = False
    tryout = 0
    i = 0
    for s in Refer_ID:
        tryout = 1
        if s.isdigit()==False:
            found = True
        if i ==0:
            i = i + 1
            found = False
        if (found==True):
            print(s)
            print(type(s))
            print (s.isdigit())

    if tryout==0:
        a = adduser(User_ID, 0)
    else:
        if found==True:
            print("tutachki")
            a = adduser(User_ID, 0)
        else:
            Refer_ID=Refer_ID[1:]
            print("tutkeckii")
            a =adduser(User_ID, Refer_ID)

    bot.send_message(message.chat.id, text='Вы пригласили: '+str(a)+' человек\nВаша ссылка для приглашения: t.me/CheckPythoBot?start='+ str(User_ID), reply_markup=MainMarkup)


bot.polling(none_stop=True)