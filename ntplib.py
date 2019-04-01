from socket import *
import ubinascii
import ustruct
#import datetime
import utime

HOST='0.uk.pool.ntp.org'
PORT=123
_PACKET_FORMAT = "!BBBbIIIIIIIIIII"

def asmNtpRequest():
    buf = bytearray(48)
    buf[0] = 0b11100011
    buf[1] = 0     # Stratum, or type of clock
    buf[2] = 6     # Polling Interval
    buf[3] = 0xEC  # Peer Clock Precision
    buf[12] = 1
    buf[13] = 2
    buf[14] = 3
    buf[15] = 4

    ubinascii.hexlify(buf).upper()
    return buf

def parseNtpResponse(data):
    ubinascii.hexlify(data[40:44])
    try:
        unpacked = ustruct.unpack(_PACKET_FORMAT,
                    data[0:ustruct.calcsize(_PACKET_FORMAT)])
    except ustruct.error:
        print("struct unpack error")
    ntp = unpacked[-2]
    ntp = ntp - 2208988800
    utime.localtime(ntp)

def settime():
    s = socket(AF_INET,SOCK_DGRAM)
    s.connect(('194.80.204.184',123))
    message = asmNtpRequest()
    s.send(message)
    data = s.recv(48)
    ubinascii.hexlify(data).upper()
    parseNtpResponse(data)
    s.close()