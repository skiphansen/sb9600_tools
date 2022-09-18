# SB9600 tools

https://github.com/skiphansen/sb9600_tools

## What is this?

Tools to assist in understanding the SB9600 protocol used by many 
Motorola radios.

## Background
Due to changing licensing requirements there are a ton of surplus Motorola 
radios which are no longer legal for use in the land mobile radios service 
(commercial "two way" radio). 

**However** these radios may still be used on Ham radio bands.  A large 
number of hams have been reverse engineering surplus Motorola radios to 
allow them to be used on Ham bands for many years.

Understanding the SB9600 protocol is key to understanding how these
radios are programmed and how they might be remotely controlled.

## SB9600 sniffer

The sniff_sn9600.py script provides the ability to capture and decode SB9600
traffic.

```
usage: sniff_sb9600.py [-h] [-f FILE] [-p PORT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --File FILE  save data to file
  -p PORT, --Port PORT  Serial port
  -v, --Verbose         print received data
skip@Dell-7040:~/SB9600/sb9600_tools$
```

Here's an example of monitoring the SB9600 bus of a Spectra when it is turned
on:

```
skip@Dell-7040:~/SB9600/sb9600_tools$ ./sniff_sb9600.py -p /dev/ttyS0
00 00 05 3B 0D: PRUPST
00 00 01 3B 36: PRUPST
01 00 00 15 A0: RADRDY
01 00 04 1F 23: ACTMDU mode 4, 00
01 00 C0 1B D0: TXAUD unmute mic, SUBAUDIO, AUDIO, PRIORITY 0, disconnect TXAUD line
05 03 07 0A 18: SETBUT Spectra Dim/Backlight, 0x07
00 01 00 0A C8: SETBUT HUB, 0x00
01 3A 00 0A 8A: SETBUT Undefined button 0x13a, 0x00
00 02 01 0A 31: SETBUT ignition sense, 0x01
01 04 00 3C 27: DISPLY 0x04, 0x00,
01 39 00 0A 1A: SETBUT Undefined button 0x139, 0x00
01 FF 0A 3C 5E: DISPLY 0xff, 0x0a,
01 38 00 0A 6A: SETBUT Undefined button 0x138, 0x00
01 FF 04 3C C1: DISPLY 0xff, 0x04,
01 FF 41 3C 1D: DISPLY 0xff, "A"
01 FF 56 3C 71: DISPLY 0xff, "V"
01 FF 4C 3C 39: DISPLY 0xff, "L"
01 FF 20 3C BD: DISPLY 0xff, " "
01 FF 44 3C 4F: DISPLY 0xff, "D"
01 FF 41 3C 1D: DISPLY 0xff, "A"
01 FF 54 3C A3: DISPLY 0xff, "T"
01 FF 41 3C 1D: DISPLY 0xff, "A"
01 FF 13 3C AD: DISPLY 0xff, 0x13,
01 FF 0B 3C 37: DISPLY 0xff, 0x0b,
^CTraceback (most recent call last):
  File "./sniff_sb9600.py", line 62, in <module>
    byte = com_port.read(1)
  File "/usr/lib/python3/dist-packages/serial/serialposix.py", line 483, in read
    ready, _, _ = select.select([self.fd, self.pipe_abort_read_r], [], [], timeout.time_left())
KeyboardInterrupt
```
## Suntor X9000 swiss army knife

The x9000.py script can be used to read and save the X9000's firmware and code plug over the SB9600 bus.  

Other functions coming soon.

```
skip@Dell-7040:~/xcat/SB9600/sb9600_tools$ ./x9000.py
usage: x9000.py [-h] [-r] [-w] [--readFirmware] [-f FILE] [-s] [--EEPROM] [-p PORT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -r, --read            Read code plug from radio
  -w, --write           Write code plug to radio
  --readFirmware        Save EPROM (firmware) into file
  -f FILE, --File FILE  file for read and write commands
  -s, --sniff           sniff SB9600 bus, listen Save code plug into file
  --EEPROM              Display size of EEPROM
  -p PORT, --Port PORT  Serial port
  -v, --Verbose         be chatty
````

## SB9600 decoder

The decode_sb9600.py script can be used to decode SB9600 data from a raw
capture file.

## sb9600 common

These scripts use Paul Bank's sb9600.py routine for CRC validation.  Thanks Paul!

## SB9600 links

- [Paul Banks article and code: Remote controlling GM1200 radio](https://paulbanks.org/projects/sb9600)
- [W3AXL: XTL5000 remote control via web](https://github.com/W3AXL/python-radio-console/wiki/Setup)
- [W3AXL: experiments with SB9600 on the XTL series](https://github.com/W3AXL/XTL-SB9600-Playground)
- [KK6JYT: Motorola Radius Programming in Windows with RSS and DOSBox](https://kk6jyt.com/motorola-radius-gm300-programming)
- [Sandy Ganz: Code to Generate SB9600 CRC](https://github.com/sganz/SB9600-CRC-Gen)
- [hamvoip article: Programming Motorola Radios with a Raspberry Pi](https://hamvoip.org/hamradio/motorola_programming)
- [SB9600 patent US5551068A (expired 8/27/2013)](https://patents.google.com/patent/US5551068A/en)
- [SB9600 patent US4637022A (expired 12/21/2004)](https://patents.google.com/patent/US4637022A/en)

