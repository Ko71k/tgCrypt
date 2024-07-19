import subprocess
from telebot import TeleBot
from telebot import types
#add your token here
#TODO: #from config import TOKEN
bot = TeleBot('token')
age = 0
name = "Alex"

@bot.message_handler(content_types=['text', 'document'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Не помогу, нечем")
    else:
        global age
        f = open("inputdata", "w")
        f.write(message.text)
        f.close()
        #encrypt(message)
        #decrypt(message)
        keyboard = types.InlineKeyboardMarkup() #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data="yes") #кнопка «Да»
        key_no  = types.InlineKeyboardButton(text='Нет', callback_data="no")
        keyboard.add(key_yes, key_no) #добавляем кнопку в клавиатуру
        question = 'Тебе '+str(age)+' лет?'
        bot.send_message(message.chat.id, text=question, reply_markup=keyboard)

def encrypt(message):
    subprocess.run("encrypt.exe inputdata Alex encrypteddata", shell = True)
    bot.send_message(message.from_user.id, 'data encrypted')

def decrypt(message):
    subprocess.run("decrypt.exe encrypteddata Alex", shell = True) #to decrypted.txt
    f = open("decrypted.txt", "r")
    bot.send_message(message.from_user.id, f.read())

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id  
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Да')
    elif call.data == "no":
        #переспрашиваем
        bot.send_message(call.message.chat.id, 'Нет')
    bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text='Принято!') 
bot.polling(none_stop=True, interval=0)