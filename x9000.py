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

def Memacs(bus,enter,reset):
    if enter:
        # Send MEMACS with exit normal bus activity
        param = 1
        if not reset:
        # Set bit 0x02 to avoid a reset when we resume busy activity
            param2 = 3
        bus.sb9600_send(0,param2,1,0x08)
        getresponse(bus)
    else:
        param = 0
        if not reset:
        # Set bit 0x02 to avoid a reset when we resume busy activity
            param2 = 0x80
        bus.sb9600_send(0,param2,1,0x08)

def ReadData(bus,args,read_type):
    if not args.InFile:
        print('Error: input filename required')
        return
    File = args.InFile
    Memacs(bus,True,False)
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

    # Resume normal bus activity without reset
    Memacs(bus,False,False)
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
        adr += 1
        bytes_written += 1

    # Verify write
    tries = 0
    while tries < 3:
        verify_block = read_block(bus,start,write_len)
        tries += 1
        if data_block == verify_block:
            print(f'Read back passed')
            break
    if tries == 3:
        print(f'Read back failed')
        bytes_written = 0

    if status:
        print('\r100%')
    return bytes_written

def Test(bus):

    block = read_block(bus,0x8002,2)
    checksum = (block[0] << 8) + block[1]
    print(f'checksum 0x{checksum:04X}')
    block = read_block(bus,0x87fa,2)
    print(f'last 2 of SN {block}')
    adjustment = (block[0] << 8) + block[1]
    print(f'adjustment 0x{adjustment:04x}')
    checksum -= adjustment
    print(f'checksum 0x{checksum:04X}')
    block=bytearray('!!','ascii')
    #block[0] = 0x36
    #block[1] = 0x39
    print(f'writing {block}')
    if write_block(bus,0x87fa,block) != 2:
        print('write_block failed')
        return 0

    adjustment = (block[0] << 8) + block[1]
    print(f'adjustment 0x{adjustment:04x}')
    checksum += adjustment
    block[0] = checksum >> 8
    block[1] = checksum & 0xff
    print(f'checksum 0x{checksum:04X}, {block}')

    if write_block(bus,0x8002,block) != 2:
        print('write_block for checksum failed')


def ConvertBin2RDT(args):
    outFile = args.InFile.replace('.bin','.RDT')
    print(f'outFile {outFile}')
    try:
        fpIn = open(args.InFile,mode='rb')
        fpOut = open(outFile,mode='wb')
        block=bytearray(b'\x01')
        fpOut.write(block)
        block = fpIn.read()
        print(f'len(block) {len(block)}')
        if len(block) != 2048 and len(block) != 8192:
            print('Error: invalid file invalid, size must be 2048 or 8192 bytes')
            return
        fpOut.write(block)
        if len(block) == 2048:
        # pad out to 8K
            block=bytearray(b'\0' * 6 * 1024)
            fpOut.write(block)

        block=bytearray(b'\005\000\004TEST')
        fpOut.write(block)
        block=bytearray(b'\000' * 708)
        fpOut.write(block)
        fpIn.close()
        fpOut.close()

    except OSError as err:
        print(err)
        exit(code=err.errno)

def ConvertRTD2Bin(args):
    outFile = args.InFile.replace('.RDT','.bin')
    print(f'outFile {outFile}')
    try:
        fpIn = open(args.InFile,mode='rb')
        fpOut = open(outFile,mode='wb')
        block = fpIn.read(1)
        block = fpIn.read()
        EEPROM_len = (block[0] << 8) + block[1] + 1
        if EEPROM_len != 2048 and EEPROM_len != 8192:
            print(f'Error: EEPROM length 0x{block[0]:x}{block[1]:02x}')
            return
        fpOut.write(block[0:EEPROM_len])
        fpIn.close()
        fpOut.close()

    except OSError as err:
        print(err)
        exit(code=err.errno)

def Convert(args):
    if not args.InFile:
        print('Error: input filename required')
        return

    if args.InFile.endswith('.bin'):
        ConvertBin2RDT(args)
    elif args.InFile.endswith('.RDT'):
        ConvertRTD2Bin(args)
    else:
        print('Error: input filename extension must be ".bin" or ".RDT"')

parser = argparse.ArgumentParser()
parser.add_argument("-r","--read",help="Read code plug from radio",action="store_true")
parser.add_argument("-w","--write",help="Write code plug to radio",action="store_true")
parser.add_argument("--readFirmware",help="Save EPROM (firmware) into file",action="store_true")
parser.add_argument("--convert",help="Convert to/from RSS .RDT format",action="store_true")
parser.add_argument("-o", "--OutFile", help="output filename")
parser.add_argument("-i", "--InFile", help="input filename")
parser.add_argument("-s","--sniff",help="sniff SB9600 bus, listen Save code plug into file",action="store_true")
parser.add_argument("--EEPROM",help="Display size of EEPROM",action="store_true")
parser.add_argument("-p", "--Port", help="Serial port",default="/dev/ttyUSB0")
parser.add_argument("-v","--Verbose",help="be chatty",action="store_true")
parser.add_argument("-t",action="store_true")
parser.add_argument("--band",help='radio band from .bin file ("low", "vhf", "uhf", or "800")',action="store_true")
args = parser.parse_args()

bus = sb9600.Serial(port=args.Port,verbose=args.Verbose)

if args.read:
    ReadData(bus,args,2)
elif args.readFirmware:
    ReadData(bus,args,1)
elif args.EEPROM:
    ReadData(bus,args,3)
elif args.convert:
    Convert(args)
elif args.t:
    Memacs(bus,True,False)
    Test(bus)
    Memacs(bus,False,False)
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


