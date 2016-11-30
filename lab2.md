
Na warsztatach było trochę powtórki asm/re (można przejrzeć wykłady z http://re.disconnect3d.pl/), no i skończyliśmy eksploita z lab1:

```python
TODO: wkleic kod
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
