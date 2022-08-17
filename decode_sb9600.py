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

from sb9600 import sb9600_CRC

memacs_3_byte_mode = False
rss_packet = False


buttons = {
0x0000:"power on/off -",
0x0001:"HUB",
0x0002:"ignition sense",
0x0003:"PTT",
0x0004:"emergency",
0x0005:"horn ring VIP input",
0x0006:"(reserved for VIP)",
0x0007:"(reserved for VIP)",
0x0008:"emergency clear",
0x0009:"front/rear control",
0x000A:"multiple radio select",
0x000B:"alternate HUB",
0x0100:"zone",
0x0101:"mode",
0x0102:"volume",
0x0103:"squelch",
0x0104:"repeat/direct",
0x0105:"monitor",
0x0106:"extender",
0x0107:"RF power",
0x0108:"home",
0x0109:"radio speaker mute",
0x010D:"alarms",
0x010E:"alarms on/off",
0x010F:"alarms select",
0x0110:"radio select",
0x0111:"RSSI",
0x0112:"Spkr Routing, Fixed Volume, Fixed RF Power (Refer to Jedi Vehicular Adapter Documentation)",
0x0130:"Spectra Ctrl Head function button 0",
0x0131:"Spectra Ctrl Head function button 1",
0x0132:"Spectra Ctrl Head function button 2",
0x0133:"Spectra Ctrl Head function button 3",
0x0134:"Spectra Ctrl Head function button 4",
0x0135:"Spectra Ctrl Head function button 5",
0x0140:"Spectra Ctrl Head keypad button 0",
0x0141:"Spectra Ctrl Head keypad button 1",
0x0142:"Spectra Ctrl Head keypad button 2",
0x0143:"Spectra Ctrl Head keypad button 3",
0x0144:"Spectra Ctrl Head keypad button 4",
0x0145:"Spectra Ctrl Head keypad button 5",
0x0146:"Spectra Ctrl Head keypad button 6",
0x0147:"Spectra Ctrl Head keypad button 7",
0x0148:"Spectra Ctrl Head keypad button 8",
0x0149:"Spectra Ctrl Head keypad button 9",
0x014A:"Spectra Ctrl Head keypad button A",
0x014B:"Spectra Ctrl Head keypad button B",
0x014C:"Spectra Ctrl Head keypad button C",
0x014D:"Spectra Ctrl Head keypad button D",
0x014E:"Spectra Ctrl Head keypad button E",
0x014F:"Spectra Ctrl Head keypad button F",
0x0150:"Spectra Ctrl Head DEK A button 0",
0x0151:"Spectra Ctrl Head DEK A button 1",
0x0152:"Spectra Ctrl Head DEK A button 2",
0x0153:"Spectra Ctrl Head DEK A button 3",
0x0154:"Spectra Ctrl Head DEK A button 4",
0x0155:"Spectra Ctrl Head DEK A button 5",
0x0156:"Spectra Ctrl Head DEK A button 6",
0x0157:"Spectra Ctrl Head DEK A button 7",
0x0158:"Spectra Ctrl Head DEK B button 0",
0x0159:"Spectra Ctrl Head DEK B button 1",
0x015A:"Spectra Ctrl Head DEK B button 2",
0x015B:"Spectra Ctrl Head DEK B button 3",
0x015C:"Spectra Ctrl Head DEK B button 4",
0x015D:"Spectra Ctrl Head DEK B button 5",
0x015E:"Spectra Ctrl Head DEK B button 6",
0x015F:"Spectra Ctrl Head DEK B button 7",
0x0160:"Spectra Ctrl Head DEK C button 0",
0x0161:"Spectra Ctrl Head DEK C button 1",
0x0162:"Spectra Ctrl Head DEK C button 2",
0x0163:"Spectra Ctrl Head DEK C button 3",
0x0164:"Spectra Ctrl Head DEK C button 4",
0x0165:"Spectra Ctrl Head DEK C button 5",
0x0166:"Spectra Ctrl Head DEK C button 6",
0x0167:"Spectra Ctrl Head DEK C button 7",
0x0168:"DEK VIP In 0",
0x0169:"DEK VIP In 1",
0x0170:"DEK VIP In 2(3 per DEK)",
0x0200:"scan on/off",
0x0201:"scan mode",
0x0202:"dynamic scan functions",
0x0203:"talkback scan",
0x0300:"MPL on/off",
0x0301:"MPL code",
0x0400:"SS on/off",
0x0401:"SS continue",
0x0402:"Route/Run config, Metro",
0x0403:"Employee # config, Metro",
0x0404:"clear button, Metrocom",
0x0405:"PRTT button, Metrocom",
0x0406:"RTT button, Metrocom",
0x0407:"Data config, Metrocom",
0x0408:"Text Message Waiting",
0x0409:"Text Message Ack",
0x040A:"Clock/Status, [Time]",
0x0503:"Spectra Dim/Backlight",
0x0504:"'A4' Ctl. Head Flash Display",
0x0506:"'A4' Ctl. Head Rotary Volume Set",
0x0700:"Mech Alarms 0",
0x0701:"Mech Alarms 1",
0x0702:"Mech Alarms 2",
0x0703:"Mech Alarms 3",
0x0704:"Mech Alarms 4",
0x0705:"Mech Alarms 5",
0x0706:"Mech Alarms 6",
0x0707:"Mech Alarms 7",
0x0708:"A Mech Alarms update 0",
0x0709:"A Mech Alarms update 1",
0x070A:"A Mech Alarms update 2",
0x070B:"A Mech Alarms update 3",
0x070C:"A Mech Alarms update 4",
0x070D:"A Mech Alarms update 5",
0x070E:"A Mech Alarms update 6",
0x070F:"A Mech Alarms update 7",
0x0710:"Metro VIP input 0",
0x0711:"Metro VIP input 1",
0x0712:"Metro VIP input 2",
0x0713:"Metro VIP input 3",
0x0714:"Metro VIP update 0",
0x0715:"Metro VIP update 1",
0x0716:"Metro VIP update 2",
0x0717:"Metro VIP update 3",
0x0800:"siren on/off",
0x0801:"siren type(wail,yelp,..)",
0x0802:"PA on/off",
0x0803:"PA volume",
0x0804:"ExRd on/off",
0x0806:"ExRd on/off (external)",
0x0900:"DVP on/off",
0x0901:"DVP code",
0x0A01:"keypad status",
0x0A02:"DEK status",
0x0A15:"send program req.",
0x0A16:"repeater access",
0x0A17:"Smart VIP #1 (state 0/1)",
0x0A18:"Smart VIP #2 (state 0/1)",
0x0A19:"Smart VIP #3 (state 0/1)",
0x0A1A:"Smart VIP #4 (state 0/1)",
0x0A1B:"Smart VIP #5 (state 0/1)",
0x0A1C:"Smart VIP #6 (state 0/1)",
0x0B01:"keypad message",
0x0B02:"DEK message",
0x0B13:"call alert",
0x0B14:"private call",
0x0B19:"one button call alert",
0x0C01:"destination (sel call)",
0x0C02:"unit to unit call",
0x0C03:"keypad H/L alarms",
0x0C05:"ind. H/L alarms on/off",
0x0C06:"ind. H/L alarms select",
0x0C07:"uni",
0x0C08:"prvt. page",
0x0C0B:"rptr. select",
0x0D01:"MVS functions",
0x0E01:"conv. phone",
0x0F01:"conv. dtmf",
0x1005:"AMSS lock",
0x1006:"AMSS site",
0x1007:"trunking status",
0x1008:"trunking message",
0x1009:"DEK trunking status",
0x100A:"DEK trunking message",
0x100E:"send rprgm. req.",
0x100F:"pac on/off",
0x1010:"system wide on/off",
0x1101:"trunking phone",
0x1103:"call alert",
0x1106:"private call",
0x1107:"conv. dtmf page",
0x1108:"one button call alert",
0x1300:"penn state rpt on/off",
0x1400:"single tone on/off"
}

addresses = {
0x00:"BroadcastSYSTEM",
0x01:"RADIO",
0x02:"DSP",
0x03:"MPL",
0x04:"INTERNAL RADIO OPTIONS",
0x05:"FRONT CONTROL HEAD",
0x06:"REAR CONTROL HEAD",
0x07:"CONTROL HEAD EXTENSIONS",
0x08:"Siren/PA",
0x09:"Securenet",
0x0A:"Emergency",
0x0A:"Status/ID",
0x0B:"Message",
0x0B:"MDC1200 SelCall",
0x0C:"MDC600 SelCall",
0x0D:"MVS Emergency",
0x0D:"MVS ID",
0x0D:"MVS Audio",
0x0E:"Phone",
0x0F:"DTMF",
0x10:"Trunking System",
0x11:"Trunking Options",
0x12:"Vehicular Repeater",
0x12:"SP Repeater",
0x13:"SP Repeater",
0x14:"Single Tone",
0x15:"Single Tone",
0x16:"Vehicle Location",
0x17:"KDT Terminal",
0x18:"Trunked deskset",
0x19:"Metrocom",
0x1A:"Control Host (see note)",
0x1B:"Vehicular Adapters"
}

        
def decode_adr(data):
    group = (data >> 5) & 0x7
    device = data & 0x1f
    print(format(group,"#x") + ":" + format(device,'#x'),end="")

def decode_MEMACS(packet):
    global rss_packet, memacs_3_byte_mode
    
    rss_packet = True
    print(" -> ",end="")
    decode_adr(packet[2])
    if packet[1] & 1:
        print(" exit bus activity to access ",end="")
    else:
        print(" resume normal bus activity after accessing ",end="")

    d3d2=(packet[1] >> 1) & 3
    if d3d2 == 0:
        print("EEPROM",end="")
    elif d3d2 == 1:
        print("RAM",end="")
    elif d3d2 == 2:
        print("OPTION DEVICE 1",end="")
    elif d3d2 == 3:
        print("OPTION DEVICE 2",end="")

    if packet[1] & 0x8:
        print(", virtual mem",end="")
    else:
        print(", physical mem",end="")

    if packet[1] & 0x10:
        print(", 3 data bytes",end="")
        memacs_3_byte_mode = True
    else:
        print(", 1 data byte",end="")
        memacs_3_byte_mode = False

    if packet[1] & 0x20:
        print(", EEPROM lock",end="")

    if packet[1] & 0x40:
        print(", Adr encryption",end="")

    if (packet[1] & 0x80) == 0:
        print(", reset",end="")


def decode_MEMADD(packet):
    global rss_packet, memacs_3_byte_mode
    print(", ",end="")

    if rss_packet: # command from rss
        if packet[3] & 0x80:
            print(f'read 0x{packet[0]:02x}{packet[1]:02x} (0x{packet[2]:02x})',end='')
        else:
            print(f'write 0x{packet[2]:02x} to 0x{packet[0]:02x}{packet[1]:02x}',end='')
    else:   # response from device
        if memacs_3_byte_mode:
            print(f'data 0x{packet[2]:02x}',end="")
            print(f' 0x{packet[1]:02x}',end="")
            print(f' 0x{packet[0]:02x}',end="")
        else:
            print(f'read adr 0x{packet[0]:02x}{packet[1]:02x} (0x{packet[2]:02x})',end='')

    rss_packet = not rss_packet


def decode_button(packet):
    lookup = ((packet[0] & 0x1f) << 8) + packet[1]
    button_data = buttons.get(lookup)
    if button_data:
        print(f' {button_data}',end='')
    else:
        print(f' Undefined button 0x{lookup:02x}',end='')

def decode_DEC_INC_BUT(packet):
    decode_button(packet)

def decode_button_opcode(packet):
    decode_button(packet)
    print(f', 0x{packet[2]:02x}',end='')

def decode_DISPLY(packet):
    print(f' 0x{packet[1]:02x},',end='')
    char = chr(packet[2])
    if char.isprintable():
        print(f' "{char}"',end='')
    else:
        print(f' 0x{packet[2]:02x},',end='')

#0x0109: 0 NP LED off, PRI LED off
#0x0109: 1 NP LED on, PRI LED off
#0x0109: 2 NP LED off, PRI LED on
#0x0109: 4 NP LED off, PRI LED blink
#0x0205: 0 NP LED off, PRI LED off
#0x0205: 1 NP LED on, PRI LED off
#0x0205: 2 NP LED off, PRI LED on
#0x0205: 4 NP LED off, PRI LED blink
def decode_np_pri_led(packet):
    print('')

# 0x010D: 0 HRN/LTS display off
# 0x010D: 1 ' HORN ON '
# 0x010D: 2 ' LIGHTS ON '
# 0x010D: 3 'HRN/LTS ON '
# 0x010F: 0 HRN/LTS display off
# 0x010F: 1 ' HORN ON '
# 0x010F: 2 ' LIGHTS ON '
# 0x010F: 3 'HRN/LTS ON '
def decode_hrn_lts(packet):
    pass

#0x0401: 0 ## ' RTT ' (## Clr 3D display)
#0x0401: 1 ' PRTT '
#0x0401: 2 ' RTT RCVD '
#0x0401: 3 ' PRTT RCVD '
#0x0401: 4 # 'RTT NO ACK '
#0x0401: 5 # 'PRTT NO ACK'
#0x0401: 6 ## ' BAD ID '
#0x0401: 7 # ' ID NO ACK '
#0x0401: 8 'USE HANDSET'
#0x0401: 9 'NO TIME SET'
def decode_401(packet):
    pass

#0x0402: 0 Rt/Rn LED off
#0x0402: 1 Rt/Rn LED on, no blink
#0x0402: 2 Rt/Rn LED on, blink on
def decode_402():
    pass

#0x0403: 0 Emp# LED off
#0x0403: 1 Emp# LED on, no blink
#0x0403: 2 Emp# LED on, blink on
def decode_403():
    pass

#0x0406: 0 PRTT, RTT (both) LEDs off
#0x0406: 1 PRTT LED on, no blink; RTT LED off
#0x0406: 2 RTT LED on, no blink; PRTT LED off
#0x0406: 3 PRTT LED on, blink on; RTT LED off
#0x0406: 4 RTT LED on, blink on; PRTT LED off
def decode_406():
    pass

#0x0407: 0 Data button LED off
#0x0407: 1 Data button LED on, no blink
#0x0407: 2 Data button LED on, blink on
def decode_407():
    pass

#0x0408: 0 Text Message LED off
#0x0408: 1 Text Message LED on, no blink
#0x0408: 2 Text Message LED on, blink on
def decode_408():
    pass

#0x0409: 1 # 'MSG WAITING'
#0x0409: 2 ## 'ACK REQUIRD'
#0x0409: 3 'NO MESSAGES'
#0x0409: 4 ' ACK RCVD '
#0x0409: 5 ## ' NO ACK '
def decode_409():
    pass

#0x0171:-79 0,1 DEK VIP Out (Up to 3 DEKs with 3 VIPs each)
def decode_dek_vip_out(packet):
    pass

def decode_MODUPD(packet):
    s3_s1 = (packet[2] >> 5)
    mode = ((packet[2] & 0x1f) << 8) + packet[3]

    print(': ',end='')
    if s3_s1 == 0:
        print("ACTMDU",end='')
    elif s3_s1 == 1:
        print("ACTMDW",end='')
    elif s3_s1 == 2:
        print("RXMODE",end='')
    elif s3_s1 == 3:
        print("TRKMDU",end='')
    elif s3_s1 == 4:
        print("TXMODE",end='')
    else :
        print(f' undefined s3_s1 value 0x{s3_s1:02x}',end='')
    print(f' {mode}',end='')

def decode_ACTMDU(packet):
    print(f' mode {packet[2]}, {packet[1]:02x}',end='')


def decode_TXAUD(packet):
    data4 = (packet[2] >> 3) & 0x7
    data5 = packet[2] & 7
    if packet[1] & 0x80:
        print(' mute mic',end='')
    else:
        print(' unmute mic',end='')
    if packet[2] & 0x80:
        print(', SUBAUDIO',end='')
    if packet[2] & 0x40:
        print(', AUDIO',end='')
    print(f', PRIORITY {data4}',end='')
    if data5 == 0:
        print(', disconnect TXAUD line',end='')
    elif data5 == 1:
        print(', connect to slatter filter',end='')
    elif data5 == 2:
        print(', connect to buffer input',end='')
    else:
        print(', undefined data5 value 0x{data5:02x}',end='')

opcodes = {
    0x01:("CHINFO", "Channel information (obsolete)"),
    0x03:("MEMFRA", "Memory addr./data framed (obsolete)"),
    0x06:("EPREQ", "Expanded protocol request"),
    0x07:("MEMADD", "** memory addr./data",decode_MEMADD),
    0x08:("MEMACS", "Memory access", decode_MEMACS),
    0x09:("SHOBUT", "Show button",decode_button_opcode),
    0x0A:("SETBUT", "Set button",decode_button_opcode),
    0x0B:("INCBUT", "Increment button",decode_DEC_INC_BUT),
    0x0C:("DECBUT", "Decrement button",decode_DEC_INC_BUT),
    0x0D:("ENTBUT", "Enter configuration"),
    0x0E:("EXTBUT", "Exit configuration"),
    0x0F:("DELBUT", "Delete button",decode_button_opcode),
    0x10:("RCLBUT", "Recall button",decode_button_opcode),
    0x11:("REQBUT", "Request button",decode_button_opcode),
    0x14:("BUTPRS", "Button press",decode_button_opcode),
    0x15:("RADRDY", "Radio ready"),
    0x16:("OPTSTS", "Option status value"),
    0x17:("DEVJSR", "Device subroutine jump"),
    0x18:("PTTINH", "Ptt inhibit"),
    0x19:("RADKEY", "Radio keyed"),
    0x1A:("RXAUD", "Receive audio routing"),
    0x1B:("TXAUD", "Transmit audio routing",decode_TXAUD),
    0x1C:("ALRTTN", "Alert tone"),
    0x1D:("AUDMUT", "Audio mute"),
    0x1E:("SQLDET", "Squelch detect"),
    0x1F:("ACTMDU", "Active mode update",decode_ACTMDU),
    0x20:("TXMODE", "Transmit mode update"),
    0x21:("RXMODE", "Receive mode update"),
    0x22:("DISMUT", "Discriminator mute"),
    0x23:("PLDECT", "Pl detect"),
    0x24:("RPTDIR", "Repeat/direct"),
    0x25:("SGINFO", "Signalling information"),
    0x26:("VOLMIN", "Volume minimum"),
    0x27:("VOLVAL", "Volume value"),
    0x28:("SQLVAL", "Squelch value"),
    0x29:("ACRXPL", "Active receive pl code"),
    0x2A:("ACTXPL", "Active transmit pl code"),
    0x2B:("RXPLIN", "Receive pl mute control inhibit"),
    0x2C:("REVINH", "Reverse burst inhibit"),
    0x2D:("SCONOF", "Scan on/off (all scans)"),
    0x2E:("TXCTRL", "Transmit control"),
    0x2F:("ACTMDW", "Active mode write"),
    0x30:("UNQSCN", "Unqualify scan"),
    0x31:("TBONOF", "Talkback on/off"),
    0x32:("DEVVAL", "Deviation value"),
    0x33:("ACPRVL", "Active tx pwr value"),
    0x34:("TXLTIN", "Transmit light inhibit"),
    0x35:("ETONOF", "Extender on/off"),
    0x36:("TOTVAL", "Time-out-timer value"),
    0x37:("ACTNPL", "Active np list"),
    0x38:("ACNPLB", "Active np list blanking"),
    0x39:("ACPRI1", "Active priority 1 mode"),
    0x3A:("ACPRI2", "Active priority 2 mode"),
    0x3B:("PRUPST", "Power up status"),
    0x3C:("DISPLY", "Display",decode_DISPLY),
    0x3D:("DSPMSG", "Display message"),
    0x3E:("BATTST", "Battery status"),
    0x3F:("CHLNUM", "Channel number"),
    0x40:("TSTMOD", "Test mode"),
    0x41:("ACDADJ", "Active deviation adjust"),
    0x42:("PALIM",  "Pa limit value"),
    0x43:("OSCVAL", "Oscillator value"),
    0x44:("PRTVAL", "Port value"),
    0x45:("TRKOPC", "Trunking opcode"),
    0x46:("TRKMDU", "Trunked mode update"),
    0x47:("ALARMS", "Alarms"),
    0x48:("PWRCTL", "Power control (obsolete)"),
    0x49:("ACTSTU", "Active state update"),
    0x4A:("VRSSTU", "Vehicular repeater status update"),
    0x4B:("DATOPC", "Data opcode"),
    0x4C:("DATCHN", "Data channel"),
    0x4E:("TIMEUP", "Time update"),
    0x4F:("METINF", "Metrocom information"),
    0x50:("XFRSTR", "Transfer data start of sequence"),
    0x51:("XFRBDY", "Transfer data body of sequence"),
    0x52:("XFREND", "Transfer data end of sequence"),
    0x53:("XFRERR", "Transfer data sequence error"),
    0x54:("XTLPUL", "Processor crystal pull"),
    0x55:("DEFBUT", "Define button",decode_button_opcode),
    0x56:("SFTPT1", "Soft pot register #1"),
    0x57:("BUTCTL", "Button control",decode_button_opcode),
    0x58:("LUMCTL", "Illumination control"),
    0x59:("CNFREQ", "Configuration request"),
    0x5A:("SPAOPC", "Special applications opcode"),
    0x5B:("TESTOP", "Test opcode"),
    0x5C:("MODUPD", "Mode Update",decode_MODUPD),
}

""""
0x0000: decode_OnOff radio power relay off,on
0x0005: decode_OnOff horn transfer relay off,on OR Metrocom emer switch test off,on
0x0006: decode_OnOff horn relay off,on OR Metrocom driver speaker off,on
0x0007: decode_OnOff light relay off, on OR Metrocom PA speaker relay off,on
0x0009: decode_OnOff speaker MUTE LED off,on
0x000A: decode_OnOff [dual radio] LED off,on
0x000B: decode_OnOff PAC-RT F1/F2 (emergency steering)
0x0010: decode_OnOff Metrocom host defined output 1 (off,on)
0x0011: decode_OnOff Metrocom host defined output 2 (off,on)
0x0012: decode_OnOff Metrocom host defined output 3 (off,on)
0x0013: decode_OnOff Metrocom host defined output 4 (off,on)
0x0014: decode_OnOff Covert monitor mic relay & LED off,on
0x0017: decode_OnOff GE-STAR (PTT ID) enabled, disabled
0x0021: 1 [radio one] LED on
0x0041: 1 [radio two] LED on
0x0061: 1 [radio three] LED on
0x0101: decode_numeric ** ' MODE XXX' active mode
0x0102: decode_numeric 'VOLUME XXX'
0x0103: decode_numeric 'SQUELCH XXX'
0x0104: decode_OnOff RPT/DIR LED off,on
0x0105: 0 'MONITOR OFF'
0x0105: 1 'MONITOR ON '
0x0108: decode_OnOff Home LED off, on
0x0109: decode_np_pri_led 4 NP LED off, PRI LED blink
0x010A: decode_OnOff BUSY LED off,on
0x010B: decode_OnOff TX LED off,on
0x010C: decode_numeric ** MODE XXX SCAN mode
0x010D: decode_hrn_lts
0x010E: decode_OnOff H/L LED off/on
0x010F: decode_hrn_lts
0x0111: decode_numeric DEV XXX
0x0112: decode_numeric COMP XXX
0x0113: decode_numeric POWER XXX
0x0114: decode_numeric CURNT XXX
0x0115: decode_numeric REFOSC XXX
0x0116: decode_numeric FAIL XXX
0x0117: --- FAIL 999
0x0118: decode_numeric RSSI XXX
0x0125: decode_OnOff MONitor LED off, on
#0x0171:-79 0,1 DEK VIP Out (Up to 3 DEKs with 3 VIPs each)
0x0171: decode_dek_vip_out
0x0172: decode_dek_vip_out
0x0173: decode_dek_vip_out
0x0174: decode_dek_vip_out
0x0175: decode_dek_vip_out
0x0176: decode_dek_vip_out
0x0177: decode_dek_vip_out
0x0178: decode_dek_vip_out
0x0179: decode_dek_vip_out
0x0200: decode_OnOff SCAN LED off,on
0x0201: decode_numeric ** MODE XXX SCAN CONFIGURATION
0x0203: decode_OnOff talk back scan LED off,on
0x0204: 1 'BLANK LIST '
0x0204: 2 ' LIST FULL '
0x0205: decode_np_pri_led
0x0300: decode_OnOff MPL LED off,on
0x0301: decode_numeric ** MPL XXX
0x0400: decode_OnOff SS LED off,on
0x0401: decode_401
0x0402: decode_402
0x0403: decode_403
0x0406: decode_406
0x0407: decode_407
0x0408: decode_408
0x0409: decode_409
0x040A: --- Reserved for Clock, [Time] LED
0x040B: decode_OnOff emergency Ack LED off,on
0x0501: decode_OnOff F/R rear speaker relay off,on
0x0503: --- Rsrvd for control head dim/backlight set.
0x0502: --- ** F/R ' REMOTE ' message
0x0601: decode_OnOff F/R front speaker relay off,on
0x0800: decode_OnOff SIREN LED off,on
0x0801: 0 ' WAIL '
0x0801: 1 ' YELP '
0x0801: 2 ' HILO '
0x0801: 3 ' MANUAL '
0x0801: 4 ' EXT RADIO '
0x0801: 5 ' AIR HORN '
0x0802: decode_OnOff PA LED off,on
0x0803: decode_numeric PA VOL XXX
0x0804: 0 WAIL DEK LED
0x0804: 1 YELP DEK LED
0x0804: 2 HILO DEK LED
0x0804: 3 MANUAL DEK LED
0x0804: 4 EXT RAD DEK LED
0x0805: --- 'SPKR SHORT ' (SYS 9000 Siren Option)
0x0805: decode_OnOff PA speaker off, on (Metrocom Only)
0x0900: decode_OnOff SNET LED off,on
0x0901: decode_numeric ** CODE XXX
0x0902: 0 don't blink BUSY LED if on
0x0902: 1 blink BUSY LED if on
0x0903: 0 don't blink TX LED if on
0x0903: 1 blink TX LED if on
0x0904: --- 'KEY ERASED'
0x0905: --- reserved for key loader
0x0A01: decode_numeric ** STATUS XXX (600 & 1200)
0x0A02: 1-8 DEK LEDs (turning one on turns rest off)
0x0A03: --- NO ACK
0x0A11: 1 'STATUS RCVD'
0x0A11: 2 ## 'STS NO ACK '
0x0A11: 3 'PLEASE WAIT'
0x0A11: 4 ' NO STATUS '
0x0A12: 1-8 DEK status LEDs blink on/off
0x0A13: 0 emergency LED off
0x0A13: 1 emergency LED on
0x0A13: 2 emergency LED blink
0x0A14: 0 # stop emergency blink
0x0A14: 1 # ' EMERGENCY '(blinks)
0x0A14: 2 # ' NO EMERG '
0x0A15: 1 'DYN REG ERR'
0x0A15: 2 'DYN REG ON '
0x0A15: 3 'DYN REG OFF'
0x0A15: 4 'RQAT NO ACK'
0x0A15: 5 'REQUEST ACK'
0x0A15: 6 'PLEASE WAIT'
0x0A15: 7 'NO DYN REG '
0x0A15: 8 ' PRGM RQST '
0x0A16: 1-9 ' RPTR '
0x0B01: decode_numeric ** 'MESSAGE XXX'
0x0B02: 1-8 DEK LEDs
0x0B11: 1 'MESAGE RCVD'
0x0B11: 2 ## 'MSG NO ACK '
0x0B11: 3 'PLEASE WAIT'
0x0B11: 4 'NO MESSAGE '
0x0B12: 1-8 DEK message LEDs blink on/off
0x0B13: 1 ## ' PAGE '
0x0B13: 2 ' ID PAGED '
0x0B13: 3 'PAGE NO ACK'
0x0B13: 4 ' STORE ID '
0x0B13: 5 'PLEASE WAIT'
0x0B13: 6 'THIS UNIT '
0x0B13: 7 'BAD ID '
0x0B14: 1 ## ' CALL '
0x0B14: 2 'ID - RCVD '
0x0B14: 3 'ID - SPRVSR'
0x0B14: 4 ' ID CALLED '
0x0B14: 5 'CALL NO ACK'
0x0B14: 6 'SCRATCH PAD'
0x0B14: 7 ' STORE ID '
0x0B14: 8 'PLEASE WAIT'
0x0B14: 9 'THIS UNIT '
0x0B14: A ' UNIT BUSY '
0x0B14: B ' NO ANSWER '
0x0B14: C ' BAD ID '
0x0B14: D 'FLEET-WIDE '
0x0B14: E 'GROUP-WIDE '
0x0B14: F ' CANCELLED '
0x0B15: 1-9 # UNIT XXX
0x0B16: 1 'FLEET WIDE '
0x0B16: 2 'GROUP WIDE '
0x0B17: 1 call alert LED blinks
0x0B17: 2 private call LED blinks
0x0C01: 0 ' BASE '
0x0C01: 1 ' FLEET '
0x0C01: 2 ' GROUP '
0x0C01: 3 ' UNIT '
0x0C02: decode_numeric ** unit names with data
0x0C03: 0 'HRN/LTS OFF' (keypad)
0x0C03: 1 ' HORN ON ' (keypad)
0x0C03: 2 'LIGHTS ON ' (keypad)
0x0C03: 3 'HRN/LTS ON ' (keypad)
0x0C04: 0 ' CALL BASE ' off
0x0C04: 1 ' CALL BASE ' on
0x0C05: 0 H/L LED off (indicator)
0x0C05: 1 H/L LED on (indicator)
0x0C06: 0 HRN/LTS off (indicator)
0x0C06: 1 HORN ON (indicator)
0x0C06: 2 LIGHTS ON (indicator)
0x0C06: 3 HRN/LTS ON (indicator)
0x0C07: --- unit to unit page
0x0C08: decode_numeric ** unit names with data
0x0C09: decode_OnOff PVT LED off,on
0x0C0A: --- PVT
0x0C0B: decode_numeric repeater names with data
0x0C0C: decode_OnOff rptr led off,on
0x0D01: 0 ' PLAY '
0x0D01: 1 ' REPLAY '
0x0D01: 2 ' RECORD '
0x0D01: 3 ' SEND '
0x0D01: 4 ' OFF '
0x0D02: --- ' VOICE MSG '
0x0E01: --- 'SCRATCHPAD '
0x0E02: 1-9 ** 'PHONE XXX '
0x0E03: --- 'PHONE CALL '
0x0E04: --- 'STORE PHONE'
0x0F01: --- 'SCRATCH PAD'
0x0F02: 1-9 ** UNIT XXX X
0x0F03: --- ' CALL '
0x0F04: 1 'STORE CALL '
0x10(1:6) 02 1 ' FAILSOFT '
0x1002: 2 'OUT OF RNGE'
0x1003: decode_OnOff Emer led off,on
0x1004: 1 ' EMERGENCY ' (blinks)
0x1004: 2 'NO EMERGNCY'
0x1005: 1 'SITE LOCKED'
0x1005: 2 'SITE UNLCKED' ?
0x1006: decode_numeric ** 'SITE XXX '
0x1007: 0 'STATUS - '
0x1007: 1-8 ** 'STATUS X '
0x1008: 1-128 ** 'MESSAGE X '
0x1009: 1 'STATUS RCVD'
0x1009: 2 'MESSGE RCVD'
0x1009: 3 ' NO STATUS '
0x1009: 4 'PLEASE WAIT'
0x1009: 5 'STS NO ACK '
0x1009: 6 'MSG NO ACK '
0x100A: 1-8 DEK Status LEDs on/off
0x100B: 1-8 DEK Message LEDs on/off
0x100C: 1-8 DEK Status LEDs Blink on/off
0x100D: 1-8 DEK Message LEDs Blink on/off
0x100E: 1 'DYN REG ERR'
0x100E: 2 'NO DYN REG '
0x100E: 3 'DYN REG ON '
0x100E: 4 'DYN REG OFF'
0x100E: 5 'RQST FAILED'
0x100E: 6 ' RQST SENT '
0x100E: 7 ' RPGM RQST '
0x100F: 1 ' NOT AUTH '
0x1010: decode_OnOff SYSTEM WIDE LED off,on
0x1011: 1-X DATA DISPLAYS
0x11(1:7) 01 1 'PLEASE WAIT'
0x1101: 2 'PHONE BUSY '
0x1101: 3 'OK TO DIAL '
0x1101: 4 'ERROR 10/02'
0x1101: 5 'KEYPAD DIAL'
0x1101: 6 'PHONE CALL '
0x1101: 7 'NO SYSTEM '
0x1101: 8 'SCRATCH PAD'
0x1101: 9 'STORE PHONE'
0x1102: 1-9 ** ' PHONE X '
0x1103: 1 'ID ALERTED '
0x1103: 2 'NO ID ACK '
0x1103: 3 'STORE ID '
0x1103: 4 'NO SYSTEM '
0x1103: 5 'PLEASE WAIT'
0x1103: 6 'THIS UNIT '
0x1103: 7 'ILLEGAL ID '
0x1103: 8 'ERROR 10/02'
0x1103: 9 'ID-________'
0x1104: 1-9 ** 'UNIT ID X '
0x1105: 1 ' PAGE ' (blinks)
0x1105: 2 ' CALL ' (blinks)
0x1106: 1 ' BAD ID '
0x1106: 2 ' STORE ID '
0x1106: 3 ' ID - RCVD '
0x1106: 4 'ID - SPRVSR'
0x1106: 5 ' ID - SENT '
0x1106: 6 ' NO ANSWER '
0x1106: 7 ' EXIT '
0x1106: 8 ?
0x1106: 9 * ' CALL '
0x14(2:0) 00 0,1 Single Tone LED off,on
0x1401: 1-16 Single Tone Mode
0x1402: 1-16 Single Tone DEK LED
"""

#def decode_TXAUD(packet):

        
def DumpHex(data,no_lf=False):
    DataLen = len(data)
    first = True
    Displayed = 0
    for byte in data:
        if not first:
            print(' ',end='')

        first = False
        print(f'{byte:02X}',end='')
        Displayed += 1
        if Displayed == 16:
            Displayed = 0
            if not no_lf:
                print('')

    if not no_lf and Displayed > 0:
        print('')

def InternalTest():
    packet = bytearray(b'\x00\xd1\x01\x08\xa6')
    decode(packet)
    packet = bytearray(b'\xfb\xfb\x5c\x87\xc8')
    decode(packet)
    packet = bytearray(b'\x01\x01\x00\x0C\x76')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x0A\x3C\x5E')
    decode(packet)
    packet = bytearray(b'\x01\x00\x02\x1F\xCA')
    decode(packet)
    packet = bytearray(b'\x01\x00\xC0\x1B\xD0')
    decode(packet)
    packet = bytearray(b'\x01\x00\xC0\x1B\xD0')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x04\x3C\xC1')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x34\x3C\x6A')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x35\x3C\x03')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x33\x3C\xEA')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x2E\x3C\x22')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x34\x3C\x6A')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x30\x3C\x51')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x30\x3C\x51')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x20\x3C\xBD')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x13\x3C\xAD')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x0B\x3C\x37')
    decode(packet)
    packet = bytearray(b'\x00\x00\x05\x3B\x0D')
    decode(packet)
    packet = bytearray(b'\x00\x00\x01\x3B\x36')
    decode(packet)
    packet = bytearray(b'\x01\x00\x00\x15\xA0')
    decode(packet)
    packet = bytearray(b'\x01\x00\x04\x1F\x23')
    decode(packet)
    packet = bytearray(b'\x00\x01\x00\x0A\xC8')
    decode(packet)
    packet = bytearray(b'\x01\x3A\x00\x0A\x8A')
    decode(packet)
    packet = bytearray(b'\x01\x00\xC0\x1B\xD0')
    decode(packet)
    packet = bytearray(b'\x05\x03\x07\x0A\x18')
    decode(packet)
    packet = bytearray(b'\x01\x39\x00\x0A\x1A')
    decode(packet)
    packet = bytearray(b'\x01\x04\x00\x3C\x27')
    decode(packet)
    packet = bytearray(b'\x01\x38\x00\x0A\x6A')
    decode(packet)
    packet = bytearray(b'\x00\x02\x01\x0A\x31')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x0A\x3C\x5E')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x04\x3C\xC1')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x41\x3C\x1D')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x56\x3C\x71')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x4C\x3C\x39')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x20\x3C\xBD')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x44\x3C\x4F')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x41\x3C\x1D')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x54\x3C\xA3')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x41\x3C\x1D')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x13\x3C\xAD')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x0B\x3C\x37')
    decode(packet)
    packet = bytearray(b'\x00\x00\x05\x3B\x0D')
    decode(packet)
    packet = bytearray(b'\x00\x00\x01\x3B\x36')
    decode(packet)
    packet = bytearray(b'\x01\x00\x00\x15\xA0')
    decode(packet)
    packet = bytearray(b'\x01\x00\x04\x1F\x23')
    decode(packet)
    packet = bytearray(b'\x00\x01\x00\x0A\xC8')
    decode(packet)
    packet = bytearray(b'\x01\x3A\x00\x0A\x8A')
    decode(packet)
    packet = bytearray(b'\x01\x00\xC0\x1B\xD0')
    decode(packet)
    packet = bytearray(b'\x05\x03\x07\x0A\x18')
    decode(packet)
    packet = bytearray(b'\x01\x39\x00\x0A\x1A')
    decode(packet)
    packet = bytearray(b'\x01\x04\x00\x3C\x27')
    decode(packet)
    packet = bytearray(b'\x01\x38\x00\x0A\x6A')
    decode(packet)
    packet = bytearray(b'\x00\x02\x01\x0A\x31')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x0A\x3C\x5E')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x04\x3C\xC1')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x41\x3C\x1D')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x56\x3C\x71')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x4C\x3C\x39')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x20\x3C\xBD')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x44\x3C\x4F')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x41\x3C\x1D')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x54\x3C\xA3')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x41\x3C\x1D')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x13\x3C\xAD')
    decode(packet)
    packet = bytearray(b'\x01\xFF\x0B\x3C\x37')
    decode(packet)

def decode(data):
    DumpHex(data,True)

    if len(data) == 5:
        crc=sb9600_CRC(data)
        if crc != 0:
            print("Invalid CRC " + format(crc,'#x'))
        else:
            opcode_data=opcodes.get(data[3] & 0x7f)
            if opcode_data and len(opcode_data):
                print(f': {opcode_data[0]}',end="")
                if len(opcode_data) > 2:
                    opcode_data[2](data)
                print("")
            else:
                print("unknown opcode " + format(data[3],'#x'))

    else:
        print(f'packet with length {len(data)} not supported')

if __name__=="__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--File",help="raw file to decode")
    parser.add_argument("--Test",help="Run internal test",action="store_true")
    args = parser.parse_args()
    if args.File:
        print(f'decoding {args.File}')
        try:
            fp = open(args.File,mode='rb')
        except OSError as err:
            print(err)
            exit(code=err.errno)
        else:
            while True:
                packet = fp.read(5)
                if not (len(packet) == 5):
                    break
                decode(packet)
            fp.close()

    elif args.Test:
        InternalTest()
    else:
        parser.print_usage()

