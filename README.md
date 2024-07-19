```
gcc encrypt.c -o encrypt.exe -lcrypt32
gcc decrypt.c -o decrypt.exe -lcrypt32

.\encrypt.exe test.txt Alex encrypted.txt
.\decrypt.exe encrypted.txt Alex
```
