from machine import RTC
from machine import Pin
from machine import I2C
from ssd1306 import SSD1306_I2C
from machine import Timer
import dht

def clock_time(tim):
    timee=clockk.datetime()
    oled.fill(0)
    oled.text("Date:",0,0)
    oled.text(str(timee[0])+'-'+str(timee[1])+'-'+str(timee[2])+'-'+week[timee[3]],0,10)
    oled.text(str(timee[4])+'-'+str(timee[5])+'-'+str(timee[6]),0,20)
    
    d.measure()
    oled.text("Temperature:"+str(d.temperature())+'C',0,40)
    oled.text("Humidity:"+str(d.humidity())+'%',0,50)
    
    oled.show() 

i2c=I2C(1,sda=Pin(2),scl=Pin(3))
oled=SSD1306_I2C(128,64,i2c,addr=0X3c)

week=['Mon','Tues','Wed','Thur','Fri','Sat','Sun']
clockk=RTC()
#clockk.datetime((2022,10,30,6,17,25,0,0))

d=dht.DHT11(Pin(0))

tim=Timer(-1)
tim.init(period=300,mode=Timer.PERIODIC,callback=clock_time)

