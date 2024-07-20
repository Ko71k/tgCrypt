```
gcc encrypt.c -o encrypt.exe -lcrypt32
gcc decrypt.c -o decrypt.exe -lcrypt32

.\encrypt.exe test.txt encrypted.txt Alex
.\decrypt.exe encrypted.txt Alex
```
