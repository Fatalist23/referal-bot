from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import mysql.connector
updater = Updater(token='546132218:AAGvBSF7dI0QTxKLvwLFlKD0aaFXYBp2_Nc')
dispatcher = updater.dispatcher

def searchUser (usID):
    result = -1
    cursor.execute("SELECT counter FROM log WHERE id = (%s)",(usID))
    res = cursor.fetchall()
    print(res)
def addUser (usID):
    zero = 0
    cursor.execute("INSERT INTO log VALUES (%s,%s)", (usID,zero))
    _SQL = """select * from log"""
    cursor.execute(_SQL)
    conn.commit()

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Ваш уникальный номер для приглашений:")
    got_id = update.message.chat_id
    bot.send_message(chat_id=update.message.chat_id, text=got_id)
    addUser(got_id)
    searchUser(got_id)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

dbconfig = { 'host': '127.0.0.1',
             'user': 'seregatest',
             'password': 'seregatestpass',
             'database': 'testbase', }
conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor(buffered=True)

checknum = 8981759
searchUser(checknum)


"""res = cursor.fetchall()
for row in res:
    print(row)
cursor.close()"""

updater.start_polling()
