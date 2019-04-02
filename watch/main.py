import utime
import esp
import machine
from machine import Pin
#from machine import I2C
from ssd1306 import SSD1306_I2C
import network
from ntplib import settime
import urequests as requests
import ujson
from machine import Timer
i2c=machine.I2C(-1, sda=machine.Pin(14), scl=machine.Pin(12), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
e=0
c=0
q=1
page=2
wlanstatus=0
button = Pin(4, Pin.IN)
np = Pin(0, Pin.IN)
fp = Pin(5, Pin.IN)
wifi=network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)
ap.active(False)
oled.text("Gundami Tech", 20, 25)
oled.show()
utime.sleep(2)


def weather():  #weather
    LURL = 'http://ipinfo.io/json'
    result = requests.get(LURL).text
    j = ujson.loads(result)
    loca = j['region']
    URL = 'https://api.seniverse.com/v3/weather/now.json?key=Sc7N7OW6wil2inCFV&location='+loca+'&language=en&unit=c'
    result = requests.get(URL).text
    j = ujson.loads(result)
    location=j['results'][0]['location']['name']
    text=j['results'][0]['now']['text']
    temp=j['results'][0]['now']['temperature']
    oled.fill(0)
    oled.text(location,10,10)
    oled.text(text,30,10)
    oled.text(temp,50,10)
    oled.show()


def showtimer():
    global ms,sec
    ms=0
    sec=0
    while 1:
        if (ms%60==0):
            sec=sec+1
            ms=ms+1
            oled.fill(0)
            oled.text(sec,10,10)
            oled.text(":",20,10)
            oled.text(ms,30,10)
            oled.show()
        else:
            ms=ms+1
            oled.fill(0)
            oled.text(sec,10,10)
            oled.text(":",20,10)
            oled.text(ms,30,10)
            oled.show()


def button1():
    oled.fill(0)
    oled.show()
    button.irq(trigger=Pin.IRQ_FALLING, handler=pd)
    tim = Timer(-1)
    if (q%2 == 0):
        tim.init(period=10, mode=Timer.PERIODIC, callback=showtimer)
    else:
        tim.callback(None)
        oled.text(sec, 10, 10)
        oled.text(":", 20, 10)
        oled.text(ms, 30, 10)
        oled.show()


def pd():
    global q
    q=q+1
    button1()

def wlan():
    global wlanstatus
    try:
        wifi.active(True)
        wifi.connect('NAIVE', '01020304')
        utime.sleep(10)
        if wifi.isconnected() == True:
            wlanstatus=1
        else:
            wlanstatus=0
    except:
        pass


def timeshow():
    if weekday == 1:
        wkdd = "Monday"
    elif weekday == 2:
        wkdd = "Tuesday"
    elif weekday == 3:
        wkdd = "Wednesday"
    elif weekday == 4:
        wkdd = "Thursday"
    elif weekday == 5:
        wkdd = "Friday"
    elif weekday == 6:
        wkdd = "Saturday"
    elif weekday == 7:
        wkdd = "Sunday"
    oled.fill(0)
    oled.text(str(year), 10, 5)
    oled.text("--", 50, 5)
    oled.text(str(month), 70, 5)
    oled.text("--", 80, 5)
    oled.text(str(mday), 100, 5)
    oled.text(wkdd, 28, 25)
    oled.text(str(hour), 32, 40)
    oled.text(":", 45, 40)
    oled.text(str(minute), 55, 40)
    oled.text(":", 70, 40)
    oled.text(str(second), 80, 40)
    oled.show()


def func(v):
    global e, c ,page
    e = e + 1
    c = e % 2
    page=0


def pageup(v):
    global page
    page=page-1


def pagedown(v):
    global page
    page=page+1


oled.fill(0)
oled.text("Connecting Wifi",5,15)
oled.text("Wait For 10S...",15,35)
oled.show()
wlan()
if (wlanstatus == 1):
    oled.fill(0)
    oled.text("Connected!",20,25)
    oled.show()
    settime()
    utime.sleep(1)
else:
    oled.fill(0)
    oled.text("Network Error",10,25)
    oled.show()
    utime.sleep(1)

wifi.active(False)
count = 0
while 1:
    count = count + 1
    if (count % (60 * 60 * 2) == 0 and hour == 0):
        count = 0
        oled.fill(0)
        oled.text("Check Time...", 5, 15)
        oled.text("Wait For 8S...", 15, 35)
        oled.show()
        wlan()
        if (wlanstatus == 1):
            settime()
            oled.fill(0)
            oled.text("Time updated!", 5, 25)
            oled.show()
            utime.sleep(1)
            wifi.active(False)
        else:
            oled.fill(0)
            oled.text("Network Error", 5, 25)
            oled.show()
            utime.sleep(1)
            wifi.active(False)
    button.irq(trigger=Pin.IRQ_FALLING, handler=func)
    np.irq(trigger=Pin.IRQ_FALLING, handler=pagedown)
    fp.irq(trigger=Pin.IRQ_FALLING, handler=pageup)
    if (c==0):
        (year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()
        print(weekday)
        oled.poweron()
        timeshow()
    else:
        oled.poweroff()
    #weather
    if (page==1):
        if wlanstatus == 1:
            weather()
        else:
            oled.fill(0)
            oled.text("Network Error",10,10)
            oled.show()
    #timer
    elif (page==3):
        button1()
    #showtime
    elif (page==2):
        (year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()
        timeshow()
    elif page > 3:
        oled.fill(0)
        oled.text("final page",10,20)
        oled.show()
        page=3
    elif page<1:
        oled.fill(0)
        oled.text("first page", 10, 20)
        oled.show()
        page = 1
    esp.sleep_type(esp.SLEEP_MODEM)
    utime.sleep(1)




