```
gcc encrypt.c -o encrypt.exe -lcrypt32
gcc decrypt.c -o decrypt.exe -lcrypt32

.\encrypt.exe test.txt encrypted.txt Alex
.\decrypt.exe encrypted.txt decrypted.txt Alex
```
Для функционирования бота нужно скачать и установить Крипто Про CSP 
```
https://www.cryptopro.ru/products/other/cryptcp
```
А так же скачать с той же страницы cryptcp.x64.exe (или x86, но тогда нужно менять вызовы в боте)
И после скачанный файл положить в директорию, из которой вызывается бот.
Далее создать в директории файл config.py с содержанием вида:
```
TOKEN = "место токена"
```
Далее запустить бота через python 
```
python .\bot_controls.py
```
