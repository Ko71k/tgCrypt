import subprocess
import telebot
#add your token here
bot = telebot.TeleBot('token')
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
        encrypt(message)
        decrypt(message)

def encrypt(message):
    subprocess.run("encrypt.exe inputdata Alex encrypteddata", shell = True)
    bot.send_message(message.from_user.id, 'data encrypted')

def decrypt(message):
    subprocess.run("decrypt.exe encrypteddata Alex", shell = True) #to decrypted.txt
    f = open("decrypted.txt", "r")
    bot.send_message(message.from_user.id, f.read())

bot.polling(none_stop=True, interval=0)