import subprocess
from telebot import TeleBot
from telebot import types
import os
from config import TOKEN
#add your token here
bot = TeleBot(TOKEN)
age = 0
name = "alex31"
#@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice']) # list relevant content types
@bot.message_handler(content_types=['text', 'document'])
def get_text_messages(message):
    global name
    if message.text == "/changeCN":
        bot.send_message(message.from_user.id, "Current name is " + name)
        bot.send_message(message.from_user.id, "Enter desired CN:")
        bot.register_next_step_handler(message, changeCN)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Current name is " + name)
        bot.send_message(message.from_user.id, "/changeCN to change CN, default is none\n\n/list_certificates to assess current certificates")
    elif message.text == "/list_certificates":
        answer = subprocess.run('"c:\Program Files\Crypto Pro\CSP\certmgr.exe" -list', capture_output=True)
        parsed_answer = answer.stdout.decode('cp866').split('-------')
        #print(answer.stdout.decode('cp866').split('-------'))
        for el in parsed_answer[1:]:
            #print(el)
            bot.send_message(message.from_user.id, el)
    elif message.text:
        #Запись полученного текста в файл inputdata
        f = open("inputdata.txt", "w")
        f.write(message.text)
        f.close()
        file_name = "inputdata.txt"
        keyboard = types.InlineKeyboardMarkup() #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Encrypt', callback_data="e|" + file_name) #кнопка «Да»
        key_no  = types.InlineKeyboardButton(text='Decrypt', callback_data="d|" + file_name)
        keyboard.add(key_yes, key_no) #добавляем кнопку в клавиатуру
        question = 'What to do with data?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    elif message.document:
        #Сохранение полученного файла в локальную директорию
        file_name = message.document.file_name
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        new_file.close()
        keyboard = types.InlineKeyboardMarkup() #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Encrypt', callback_data="e|" + file_name) #кнопка «Да»
        key_no  = types.InlineKeyboardButton(text='Decrypt', callback_data="d|" + file_name)
        key_add  = types.InlineKeyboardButton(text='Add as certificate', callback_data="add_cert|" + file_name)
        keyboard.add(key_yes, key_no, key_add) #добавляем кнопку в клавиатуру
        question = 'What to do with data?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Try again")

def changeCN(message):
    global name 
    name = message.text
    text = "CN set to " + message.text
    bot.send_message(message.from_user.id, text)

def encrypt(message, file_name):
    global name
    call_encrypt = "encrypt.exe "
    call_encrypt += file_name + " "
    call_encrypt += "e" + file_name + " "
    call_encrypt += name
    subprocess.run(call_encrypt, shell = True) #to d + file_name
    try:
        f = open("e" + file_name, "rb")
        bot.send_message(message.chat.id, 'data encrypted')
        bot.send_document(message.chat.id,f)
        f.close()
        os.remove("e" + file_name)
        os.remove(file_name)
    except:
        bot.send_message(message.chat.id, "ERROR:CN not found, try /changeCN.")
        os.remove(file_name)
    
def decrypt(message, file_name):
    global name
    call_decrypt = "decrypt.exe "
    call_decrypt += file_name + " "
    call_decrypt += "d" + file_name + " "
    call_decrypt += name
    subprocess.run(call_decrypt, shell = True) #to d + file_name
    try:
        f = open("d" + file_name, "rb")
    except:
        bot.send_message(message.chat.id, "ERROR:CN not found, try /changeCN.")
        return
    try:
        f = open("d" + file_name, "rb")
        bot.send_message(message.chat.id, f.read())
        f.close()
        os.remove("d" + file_name)
        os.remove(file_name)
    except:
        f = open("d" + file_name, "rb")
        bot.send_document(message.chat.id,f)
        f.close()
        os.remove("d" + file_name)
        os.remove(file_name)

def certificate_decrypt(message, file_name):
    global name
    runner = '.\cryptcp.x64.exe -decr -dn "CN=' + name + '" ' + file_name + ' ' + 'decrypted.' + file_name + ' -nochain'
    print(runner)
    answer = subprocess.run(runner, capture_output=True, shell=True)
    bot.send_message(message.chat.id, answer.stdout.decode('cp866'))
    try:
        f = open("decrypted." + file_name, "r")
        bot.send_document(message.chat.id, f)
        f.close()
        os.remove(file_name)
        os.remove("decrypted." + file_name)
    except:
        bot.send_message(message.chat.id, "Huh, try again")
    return

def cert_encrypt(message, file_name):
    bot.send_message(message.chat.id, "Encrypting file " + file_name + "\nSend a certificate:")
    bot.register_next_step_handler(message, certificate_reciever_encrypt, file_name)

def certificate_reciever_encrypt(message, file_name1):
    if (message.document):
        cert_name = message.document.file_name
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(cert_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        new_file.close()
        runner = '.\cryptcp.x64.exe -encr -f ' + cert_name + ' ' + file_name1 + " encrypted." + file_name1 + ' -nochain'
        print(runner)
        answer = subprocess.run(runner, capture_output=True, shell=True)
        bot.send_message(message.chat.id, answer.stdout.decode('cp866'))
        try:
            f = open("encrypted." + file_name1, "rb")
            bot.send_document(message.chat.id, f)
            f.close()
            os.remove(cert_name)
            os.remove(file_name1)
            os.remove("encrypted." + file_name1)
        except:
            bot.send_message(message.chat.id, "Huh, try again")
            return
    else:
        bot.send_message(message.chat.id, "Huh, try again")
        os.remove(cert_name)
        return

def add_cert(message, file_name):
    #"c:\Program Files\Crypto Pro\CSP\certmgr.exe"
    #"c:\Program Files\Crypto Pro\CSP\certmgr.exe" -install -file alex22.pfx -pfx -silent -pin r 
    bot.send_message(message.chat.id, "Adding as a cert " + file_name + "\nEnter the password:")
    bot.register_next_step_handler(message, install_cert, file_name)

def install_cert(message, file_name):
    print("\ninstalling with file-name =", file_name)
    runner = '"c:\Program Files\Crypto Pro\CSP\certmgr.exe" -install -file ' + file_name + ' -pfx -pin ' + message.text + ' -silent'
    answer = subprocess.run(runner, capture_output=True, shell=True)
    print(runner)
    print(answer.stdout.decode('cp866'))
    bot.send_message(message.chat.id, answer.stdout.decode('cp866').split('=============================================================================')[-1])
    os.remove(file_name)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    parsed_data = call.data.split('|')
    if parsed_data[0] == "e":
        #encrypt(message, call.data[2:])
        cert_encrypt(message, call.data[2:])
    elif parsed_data[0] == "d":
        #decrypt(message, call.data[2:])
        certificate_decrypt(message, call.data[2:])
    elif parsed_data[0] == "add_cert":
        add_cert(message, parsed_data[1])

    bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text='Принято!') 
    

    
bot.polling(none_stop=True, interval=0)