
Przerobione zadania:
* http://re.disconnect3d.pl/logmein - proste zadanie z RE, które wymaga tak naprawdę zrobienia XORa dwóch stringów
* http://re.disconnect3d.pl/easy - zadanie z PWN, nieskończone - *do dokończenia w domu*

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
* x - "egzaminowanie" pamięci, wykorzystywane wraz z formatem - np. x/16xw <adres> wyświetli 16 elementów dwubajtowych (specyfikator 'w' - niefortunnie 'word' w gdb to cztery bajty) z podanego adresu zapisanych heksadecymalnie (x) 

Losowe hinty do Ida Pro/Hopper:
* klawisz 'n' na symbolu - refaktoryzacja jego nazwy
* klawisz 'x' na symbolu - szukanie xrefów
* klawisz 'y' na symbolu - zmiana jego typu (dla zdekompilowanego kodu)

Wyświetlanie stron pamięci danego procesu:
    cat /proc/<pid>/maps
    w pwndbg/peda: vmmap


## Rzeczy do zrobienia/przeczytania na kolejne laborki:
* Wykłady z http://re.disconnect3d.pl/
* http://blog.exploitlab.net/2011/12/tutorials-to-refresh-your-fundamental.html
* https://sploitfun.wordpress.com/2015/06/26/linux-x86-exploit-development-tutorial-series/
