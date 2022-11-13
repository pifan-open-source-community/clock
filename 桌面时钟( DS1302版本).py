from machine import Pin
from machine import I2C
from ssd1306 import SSD1306_I2C
from machine import Timer
import dht
from DS1302 import DS1302

def clock_time(tim):
    timee=ds.DateTime()
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



d=dht.DHT11(Pin(0))
ds = DS1302(Pin(12),Pin(13),Pin(14))
#ds.SetTime(2022,11,12,5,20,03,30)
tim=Timer(-1)
tim.init(period=300,mode=Timer.PERIODIC,callback=clock_time)

