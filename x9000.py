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

import argparse
import math
from time import sleep
from binascii import hexlify, unhexlify
import sb9600
import decode_sb9600

def get_mem_read(bus,adr):
    data_block=bytearray()
    msb = adr >> 8
    lsb = adr & 0xff
    packet = bus.read(5)
    resp_len = len(packet)
    if resp_len == 5:
        if packet[0] == msb and packet[1] == lsb and packet[3] == 0x7:
            data_block.append(packet[2])
    elif resp_len == 0:
        print('no response')
    else:
        print(f'received {resp_len} bytes')
    return data_block

def read_block(bus,start,len,status=False):
    adr = start
    end = start + len
    data_block=bytearray()
    bytes_read = 0
    last_percent = -1

    while adr < end:
        if status:
        # report status every percent
            percent = 100 * bytes_read / len
            if(percent - last_percent >= 1):
                last_percent = percent
                print(f'\r{math.floor(percent)}%',end='')
        msb = adr >> 8
        lsb = adr & 0xff
    # Send MEMADD command
        bus.sb9600_send(msb,lsb,0,0x87)
        #read response
        byte = get_mem_read(bus,adr)
        if not byte:
        # try again
            byte = get_mem_read(bus,adr)
        if not byte:
            print(f'Read failed at 0x{adr:04x}')
            data_block.clear()
            break
        data_block.append(byte[0])
        adr += 1
        bytes_read += 1
    if status:
        print('\r100%')
    return data_block

def getresponse(bus,verbose=False):
    packet = bus.read(5)
    resp_len = len(packet)
    if resp_len == 0:
        if verbose:
            print('no response')
    elif resp_len == 5:
        decode_sb9600.decode(packet)
    else:
        print(f'received {resp_len} bytes')
    return packet

def ReadData(bus,File,read_type):
    # Send MEMACS with exit normal bus activity, bit 0x02 must be set to avoid
    # a reset when we 
    bus.sb9600_send(0,0x03,1,0x08)
    getresponse(bus)

    read_len = 0;
    if read_type == 1:
    # read EPROM (firmware)
        adr = 0xc000
        read_len = 0x4000
        print(f'reading firmware, ({read_len} bytes ... this is going to take a while!)')
    elif read_type == 2 or read_type == 3:
    # read EEPROM (code plug)
        adr = 0x8000
        block = read_block(bus,adr,2)
        if not block:
            print('read failed')
        else:
            read_len = (block[0] << 8) + block[1] + 1
            if read_len == 2048 or read_len == 8192 or read_len==16384:
                if read_type == 3:
                    print(f'EEPROM size is {int(read_len / 1024)}K bytes')
                    read_len = 0
                else:
                    print(f'reading code plug, ({read_len} bytes)')
            elif read_len == 0x10000:
                print('code plug appears to be blank, ({read_len} bytes)')
                read_len = 0
            else:
                print(f'EEPROM size {read_len}???')
                read_len = 0
    else:
        print(f'internal error, invalid read_type {read_type}')

    if read_len > 0:
        block = read_block(bus,adr,read_len,status=True)
        if not block:
            print('read failed')
        else:
            print(f'read {len(block)} bytes')
            if File:
                print('saving data')
                try:
                    fp = open(File,mode='wb')
                    fp.write(block)
                    fp.close()
                except OSError as err:
                    print(err)
                    exit(code=err.errno)

    # Send MEMACS with enter normal bus activity, 
    # all we did was read so no reset is needed
    bus.sb9600_send(0,0x80,1,0x08)

def write_block(bus,start,data_block,status=False):
    adr = start
    write_len = len(data_block)
    bytes_written = 0
    last_percent = -1

    while bytes_written < write_len:
        if status:
        # report status every percent
            percent = 100 * bytes_written / write_len
            if(percent - last_percent >= 1):
                last_percent = percent
                print(f'\r{math.floor(percent)}%',end='')
        msb = adr >> 8
        lsb = adr & 0xff
    # Send MEMADD command
        byte2write = data_block[bytes_written]
        bus.sb9600_send(msb,lsb,byte2write,0x07)
        #read response
        tries = 0
        while tries < 10:
            getresponse(bus,True)
            tries += 1
        if tries == 10:
            print(f'Read back failed at 0x{adr:04x}')
            bytes_written = 0
            break

        if byte != byte2write:
            print(f'Verify error at 0x{adr:04x}, wrote 0x{byte2write:02x}  read 0x{byte:02x}')
            bytes_written = 0
            break
        adr += 1
        bytes_written += 1
    if status:
        print('\r100%')
    return bytes_written

parser = argparse.ArgumentParser()
parser.add_argument("-r","--read",help="Read code plug from radio",action="store_true")
parser.add_argument("-w","--write",help="Write code plug to radio",action="store_true")
parser.add_argument("--readFirmware",help="Save EPROM (firmware) into file",action="store_true")
parser.add_argument("-f", "--File", help="file for read and write commands")
parser.add_argument("-s","--sniff",help="sniff SB9600 bus, listen Save code plug into file",action="store_true")
parser.add_argument("--EEPROM",help="Display size of EEPROM",action="store_true")
parser.add_argument("-p", "--Port", help="Serial port",default="/dev/ttyUSB0")
parser.add_argument("-v","--Verbose",help="be chatty",action="store_true")
args = parser.parse_args()

bus = sb9600.Serial(port=args.Port,verbose=args.Verbose)

if (args.read or args.readFirmware) and not args.File:
    print('Error: filename required')
elif args.read:
    ReadData(bus,args.File,2)
elif args.readFirmware:
    ReadData(bus,args.File,1)
elif args.EEPROM:
    ReadData(bus,args.File,3)
elif args.sniff:
    pass
else:
    parser.print_help()

if args.sniff:
    print('Monitoring the SB9600 bus')
    while True:
        packet = bus.read(5)
        if len(packet) == 5:
            decode_sb9600.decode(packet)


