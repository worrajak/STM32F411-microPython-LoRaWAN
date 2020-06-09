import pyb
import utime as time
from machine import I2C
import ssd1306
import BME280
from time import sleep

sw  = pyb.Switch() # user push button
led = pyb.LED(1)   # on-board LED (blue), PC13 pin

rtc = pyb.RTC()

i2c = I2C(-1, scl=pyb.Pin.board.PB6, sda=pyb.Pin.board.PB7, freq=100000)

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
bme = BME280.BME280(i2c=i2c)
led.on()

try:
    while not sw.value():
        dt = rtc.datetime()
        temp = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        print('Temperature: ', temp)
        print('Humidity: ', hum)
        print('Pressure: ', pres)
        print(rtc.datetime())     
        print()
        
        oled.text('OLED BME280', 0, 0)
        oled.text(temp, 0, 20)
        oled.text(hum, 60, 20)
        oled.text("Time:{0:02}:{1:02}:{2:02}".format(dt[4],dt[5],dt[6]),0,40)
        oled.text("Date:{0:02}/{1:02}/{2:02}".format(dt[2],dt[1],dt[0]),0,50)
        oled.show()

        sleep(5)
        oled.fill(0)
except KeyboardInterrupt:
    pass
finally:
    led.off() # turn off LED
    print('Done')
