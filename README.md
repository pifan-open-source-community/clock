```bash
代码仓库
1、码云Gitee：https://gitee.com/yangkun_monster/clock.git
2、Github：https://github.com/pifan-open-source-community/clock.git

视频教程地址：
哔哩哔哩bilibili：树莓派爱好者基地、玩派VLOG

视频VLOG记录：
哔哩哔哩bilibili：玩派VLOG

```

## 一、概述

用树莓派PICO做一个桌面时钟，可显示年、月、日、时、分、秒、星期、温度、湿度。时钟分为两种，一种是使用内置RTC函数，另一种是使用DS1302时钟模块，可以根据自己情况选择（时钟模块具有备用电池，可以保证在断电的情况下持续走时）

编程语言： micropython。

## 二、材料准备
### 1、树莓派PICO
![在这里插入图片描述](https://img-blog.csdnimg.cn/d71c14b9748e4dc0bc1396df759f00e8.jpeg#pic_center)
PICO接口图
![在这里插入图片描述](https://img-blog.csdnimg.cn/08367390ddb541af9775aea0261e0644.png#pic_center )
### 2、DHT11温湿度传感器
DHT11是一款有已校准数字信号输出的温湿度传感器。 其精度湿度±5%RH， 温度±2℃，量程湿度5~95%RH， 温度-20～+60℃。
![在这里插入图片描述](https://img-blog.csdnimg.cn/75dae6cd4b8249339321b624c3ff1b8a.png#pic_center)
### 3、DS1302时钟模块（选用）
DS1302时钟芯片是由美国DALLAS公司推出的具有涓细电流充电能力的低功耗实时时钟芯片。它可以对年、月、日、周、时、分、秒进行计时，且具有闰年补偿等多种功能。DS1302芯片包含一个用于存储实时时钟/日历的 31 字节的静态 RAM，可通过简单的串行接口与微处理器通讯，将当前的是时钟存于RAM。DS1302芯片对于少于 31 天的月份月末会自动调整,并会自动对闰年进行校正。
![在这里插入图片描述](https://img-blog.csdnimg.cn/767d61290d2e46929783520397640513.jpeg#pic_center)
引脚说明 
![在这里插入图片描述](https://img-blog.csdnimg.cn/173eb10d8ad64dd8ab60d25befc9f8d4.png#pic_center)
寄存器（选看）
![在这里插入图片描述](https://img-blog.csdnimg.cn/6978296601074a37a697b391d8e6e535.png#pic_center)
读地址为0x81（秒）, 0x83（分）, 0x85（时）, 0x87（日）, 0x89（月）, 0x8b（星期）, 0x8d（年）
写地址为0x80（秒）, 0x82（分）, 0x84（时）, 0x86（日）, 0x88（月）, 0x8a（星期）, 0x8c（年）
### 4、SSD1306屏幕
![在这里插入图片描述](https://img-blog.csdnimg.cn/7f3facecfeac4917a0195e199bb83be4.jpeg#pic_center)
通信方式为IIC

### 5、其他材料
面包板
![在这里插入图片描述](https://img-blog.csdnimg.cn/bc6858566fb049d9bd99a0660c94e1de.webp#pic_center)

公对母杜邦线
![在这里插入图片描述](https://img-blog.csdnimg.cn/f4ef760313134c63b0ee3ebf1f6f4afe.webp#pic_center)
## 三、开始
### 1、连线
| DTH11 |  |
|--|--|
| VCC |  |
|GND| |
|DATA| GP0|

| SSD1306 |  |
|--|--|
| VCC |  |
|GND| |
|SCL| GP3|
|SDA| GP2|

| DS1302 |  |
|--|--|
| VCC |  |
|GND| |
|CLK| GP12|
|DAT| GP13|
|RST| GP14|

![在这里插入图片描述](https://img-blog.csdnimg.cn/a80d7b6bde37487c9c86e0948b376a56.png#pic_center)

### 2、写程序
#### （1）使用内置RTC函数实现的时钟
该时钟在PICO连接电脑使用时可以自动读取电脑的时间，在PICO断电后时钟会暂停，不能持续走时。

```python
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
#clockk.datetime((2022,10,30,6,17,25,0,0))#设置初始时间，年、月、日、星期、时、分、秒

d=dht.DHT11(Pin(0))

tim=Timer(-1)
tim.init(period=300,mode=Timer.PERIODIC,callback=clock_time)
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/514780b5179e4beea566fc64539443a0.png#pic_center)

#### （2）使用DS1302时钟模块实现的时钟
时钟模块具有备用电池，可以保证在断电的情况下持续走时

主程序

```python
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
#ds.SetTime(2022,11,12,5,20,03,30)#设置初始时间，年、月、日、星期、时、分、秒
tim=Timer(-1)
tim.init(period=300,mode=Timer.PERIODIC,callback=clock_time)
```

DS1302库

```python
'''
    DS1302 RTC drive

    Author: shaoziyang
    Date:   2018.3

    http://www.micropython.org.cn
'''
from machine import *

DS1302_REG_SECOND = (0x80)
DS1302_REG_MINUTE = (0x82)
DS1302_REG_HOUR   = (0x84)
DS1302_REG_DAY    = (0x86)
DS1302_REG_MONTH  = (0x88)
DS1302_REG_WEEKDAY= (0x8A)
DS1302_REG_YEAR   = (0x8C)
DS1302_REG_WP     = (0x8E)
DS1302_REG_CTRL   = (0x90)
DS1302_REG_RAM    = (0xC0)

class DS1302:
    def __init__(self, clk, dio, cs):
        self.clk = clk
        self.dio = dio
        self.cs  = cs
        self.clk.init(Pin.OUT)
        self.cs.init(Pin.OUT)
        
    def DecToHex(self, dat):
        return (dat//10) * 16 + (dat%10)

    def HexToDec(self, dat):
        return (dat//16) * 10 + (dat%16)

    def write_byte(self, dat):
        self.dio.init(Pin.OUT)
        for i in range(8):
            self.dio.value((dat >> i) & 1)
            self.clk.value(1)
            self.clk.value(0)

    def read_byte(self):
        d = 0
        self.dio.init(Pin.IN)
        for i in range(8):
            d = d | (self.dio.value()<<i)
            self.clk.value(1)
            self.clk.value(0)
        return d

    def getReg(self, reg):
        self.cs.value(1)
        self.write_byte(reg)
        t = self.read_byte()
        self.cs.value(0)
        return t

    def setReg(self, reg, dat):
        self.cs.value(1)
        self.write_byte(reg)
        self.write_byte(dat)
        self.cs.value(0)

    def wr(self, reg, dat):
        self.setReg(DS1302_REG_WP, 0)
        self.setReg(reg, dat)
        self.setReg(DS1302_REG_WP, 0x80)
                
    def start(self):
        t = self.getReg(DS1302_REG_SECOND + 1)
        self.wr(DS1302_REG_SECOND, t & 0x7f)

    def stop(self):
        t = self.getReg(DS1302_REG_SECOND + 1)
        self.wr(DS1302_REG_SECOND, t | 0x80)
        
    def Second(self, second = None):
        if second == None:
            return self.HexToDec(self.getReg(DS1302_REG_SECOND+1))%60
        else:
            self.wr(DS1302_REG_SECOND, self.DecToHex(second%60))

    def Minute(self, minute = None):
        if minute == None:
            return self.HexToDec(self.getReg(DS1302_REG_MINUTE+1))
        else:
            self.wr(DS1302_REG_MINUTE, self.DecToHex(minute%60))

    def Hour(self, hour = None):
        if hour == None:
            return self.HexToDec(self.getReg(DS1302_REG_HOUR+1))
        else:
            self.wr(DS1302_REG_HOUR, self.DecToHex(hour%24))

    def Weekday(self, weekday = None):
        if weekday == None:
            return self.HexToDec(self.getReg(DS1302_REG_WEEKDAY+1))
        else:
            self.wr(DS1302_REG_WEEKDAY, self.DecToHex(weekday%8))

    def Day(self, day = None):
        if day == None:
            return self.HexToDec(self.getReg(DS1302_REG_DAY+1))
        else:
            self.wr(DS1302_REG_DAY, self.DecToHex(day%32))

    def Month(self, month = None):
        if month == None:
            return self.HexToDec(self.getReg(DS1302_REG_MONTH+1))
        else:
            self.wr(DS1302_REG_MONTH, self.DecToHex(month%13))

    def Year(self, year = None):
        if year == None:
            return self.HexToDec(self.getReg(DS1302_REG_YEAR+1)) + 2000
        else:
            self.wr(DS1302_REG_YEAR, self.DecToHex(year%100))

    def DateTime(self, dat = None):
        if dat == None:
            return [self.Year(), self.Month(), self.Day(), self.Weekday(), self.Hour(), self.Minute(), self.Second()]
        else:
            self.Year(dat[0])
            self.Month(dat[1])
            self.Day(dat[2])
            self.Weekday(dat[3])
            self.Hour(dat[4])
            self.Minute(dat[5])
            self.Second(dat[6])

    def ram(self, reg, dat = None):
        if dat == None:
            return self.getReg(DS1302_REG_RAM + 1 + (reg%31)*2)
        else:
            self.wr(DS1302_REG_RAM + (reg%31)*2, dat)
            
    def SetTime(self,YEAR,MONTH,DAY,WEEK,HOUR,MINUTE,SECOND,):
        self.Year(YEAR)
        self.Month(MONTH)
        self.Day(DAY)
        self.Weekday(WEEK)
        self.Hour(HOUR)
        self.Minute(MINUTE)
        self.Second(SECOND)
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/4709300797e242de9907dd26a0622d2a.png#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/b3535e1a2d8a48b59b033b4e461fc292.png#pic_center)
