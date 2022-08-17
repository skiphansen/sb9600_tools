#!/bin/env python3
#
# Copyright (C) 2022 Skip Hansen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# The latest version of this program may be found at
# https://github.com/skiphansen/sb9600_tools

import serial
import argparse
import decode_sb9600
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--File", help="save data to file")
parser.add_argument("-p", "--Port", help="Serial port",default="/dev/ttyUSB0")
parser.add_argument("-v","--Verbose",help="print received data",action="store_true")
args = parser.parse_args()

# Open serial port
try:
    com_port = serial.Serial(args.Port,baudrate=9600,timeout=0)
except OSError as err:
    print(err)
    exit(code=err.errno)

if args.File:
# Open file
    try:
        fp = open(args.File,mode='wb')
    except OSError as err:
        print(err)
        exit(code=err.errno)


# drop busy out
com_port.setDTR(0)
busy = com_port.cts

packet=bytearray()

busy = com_port.cts
lastBusy = busy
if args.Verbose:
    print(f'Initial busy {busy}')

while True:
    byte = com_port.read(1)
    busy = com_port.cts
    Received = len(byte)
    if Received > 1:
        print(f'Received {Received}, aborting')
        break

    if lastBusy != busy:
        lastBusy = busy
        if busy:
            packet.clear()
            if args.Verbose:
                print("Busy")

    if Received == 1:
        packet.append(byte[0])
        if args.Verbose:
            print(f'0x{byte[0]:02X}',end=' ')

    if len(packet) == 5:
        if args.Verbose:
            print('')
        if args.File:
            fp.write(packet)
        decode_sb9600.decode(packet)
        packet.clear()


