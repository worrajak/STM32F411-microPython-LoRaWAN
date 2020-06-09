# STM32F411-microPython-LoRaWAN


#ESP32 AT
#from pyb import UART
import bme280, time, ubinascii, machine
from machine import UART, Pin, I2C
from struct import unpack
from cayennelpp import CayenneLPP
temp = 25.5
pa = 102000
hum = 40.5
#i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
#bme = bme280.BME280(i2c=i2c)
uart = UART(2, 115200,timeout=2000)
uart.write("AT+NRB\r\n")
print(uart.read()) 
time.sleep(10.0)
uart.write("AT\r\n")
print(uart.read())
uart.write("AT+ADDR=26041F43\r\n")
print(uart.read())
uart.write("AT+APPSKEY=7E95A0280C659A07B30A4E3CA4CF06EC\r\n")
print(uart.read())
uart.write("AT+NWKSKEY=CAD5B1896490A1B402A0BDA6AFD86991\r\n")
print(uart.read()) 
uart.write("AT+ACTIVATE=0\r\n") #ABP Activate
print(uart.read())

cnt = 1
while True:
   print("Packet No #{}".format( cnt ) )
   #temp,pa,hum = bme.values 
   print("********BME280 values:")
   print("temp:",temp," Hum:",hum ,"PA:", pa)
   c = CayenneLPP()
   c.addTemperature(1, float(temp)) 
   c.addRelativeHumidity(2, float(hum)) 
   c.addBarometricPressure(3, float(pa)) 
   d = (ubinascii.hexlify(c.getBuffer()))
   print(" — — — — -Start Send Status — — — — — — ")
   print("AT+NMGS={0},{1}\r\n".format(int(len(d)/2),(d.decode("utf-8"))))
   uart.write("AT+NMGS={0},{1}\r\n".format(int(len(d)/2),(d.decode("utf-8"))))
   print(uart.read())
   print("— — — — -End Send Status — — — — — — ")
   cnt = cnt + 1 
   time.sleep(60.0)
