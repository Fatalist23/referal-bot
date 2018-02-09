from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import mysql.connector
updater = Updater(token='546132218:AAGvBSF7dI0QTxKLvwLFlKD0aaFXYBp2_Nc')
dispatcher = updater.dispatcher
dbconfig = { 'host': '127.0.0.1',
             'user': 'seregatest',
             'password': 'seregatestpass',
             'database': 'testbase', }

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor(buffered=True)

#hello Friday
def searchuser (usID):
    userCounter = -1
    cursor.execute("SELECT refCount FROM users WHERE userID =" + str(usID))
    res = cursor.fetchall()
    userCounter = res[0][0]
    return userCounter

def ifrefed (usID):
    wasrefed = False
    cursor.execute("SELECT ifInv FROM users WHERE userID =" + str(usID))
    res = cursor.fetchall()
    if ((res[0][0])==1):
        wasrefed = True
    return wasrefed


def adduser (usID):
    cursor.execute("INSERT INTO users VALUES (%s,%s,%s)", (usID, 0, 0))
    conn.commit()


def adduserref (usID, refID):

    cursor.execute("INSERT INTO users VALUES (%s,%s,%s)", (usID, 0, 1))



def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Ваш уникальный номер для приглашений:")
    got_id = update.message.chat_id
    bot.send_message(chat_id=update.message.chat_id, text=got_id)
    adduser(got_id)
    ifrefed(got_id)
    searchuser(got_id)


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)



checknum = 8981759
#searchuser(checknum)


"""res = cursor.fetchall()
for row in res:
    print(row)
cursor.close()"""

updater.start_polling()
