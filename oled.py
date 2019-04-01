"""
# -*- coding: utf-8 -*-
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageDraw, Image,ImageFont
import time

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

while True:
    with canvas(device) as draw:
        #font1=ImageFont.load_default(20)
        font1= ImageFont.truetype('Gotham-Book.ttf',14)
        # draw.rectangle(device.bounding_box, outline="white", fill="black")
        #draw.text((30, 2), "System ok", fill="white")
        #draw.text((5, 20), "No face is found",font=font1, fill="white")
        size = (0, 15, 128, 64)
        device.fill(1)
        #draw.rectangle(size, fill=225)
        time.sleep(2)
        #size = (0, 15, 128, 64)
        #draw.rectangle(size, fill=0)
        #time.sleep(2)
"""
# !/usr/bin/env python

import main
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageDraw, Image, ImageFont
import threading
import inspect
import ctypes


device = ssd1306(port=1, address=0x3C)
font2 = ImageFont.truetype('Gotham-Book.ttf', 12)


def show(d):
    with canvas(d) as draw:
        draw.text((40, 1),'System ok', fill=225)
        draw.text((5, 20), 'No face is detected', font=font2, fill=225)


def clean(d):
    with canvas(d) as draw:
        draw.rectangle((0, 15, 128, 64), outline=0, fill=0)


def show1(d):
    with canvas(d) as draw:
        draw.text((40, 1),'System ok', fill=225)
        draw.text((5, 20), 'Welcome CYY', font=font2, fill=225)


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def showtime():
    nowDt = datetime.datetime.now() + datetime.timedelta(hours=8)
    while True:
        tm = nowDt.strftime('%H:%M:%S')
        with canvas(device) as draw:
            draw.text((10, 40), tm, font=font2, fill=225)
        nowDt = nowDt + datetime.timedelta(seconds=1)
        main.sleep(1)


def main():
    while True:
        show(device)
        #clean(device)
        showtime(device)
        #clean(device)


if __name__ == "__main__":
    t = threading.Thread(target=main)
    t.start()
    main.sleep(10)
    print("stoped")
    stop_thread(t)

