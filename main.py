import pyb
import ure
import BME280, time, ubinascii, machine
from machine import UART, Pin, I2C
from struct import unpack
from cayennelpp import CayenneLPP

adc = pyb.ADCAll(12)    # create an ADCAll object
rtc = pyb.RTC()
rtc.wakeup(60000)
led = pyb.LED(1)

temp = 0.0
pa = 0.0
hum = 0.0

i2c = I2C(scl=pyb.Pin.board.PB6, sda=pyb.Pin.board.PB7, freq=10000)
#i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))

bme = BME280.BME280(i2c=i2c)
uart = UART(2, 115200,timeout=2000)
#uart.write("AT+NRB\r\n")
#print(uart.read())


time.sleep(2.0)

#TTN115 F411 DL7612-AS923 
#uart.write("AT\r\n")
#print(uart.read())
#uart.write("AT+ADR?\r\n")
#print(uart.read())
#uart.write("AT+DR=0\r\n")
#print(uart.read())
#uart.write("AT+CLASS?\r\n")
#print(uart.read())
uart.write("AT+ADDR=26041F43\r\n")
print(uart.read())
uart.write("AT+APPSKEY=7E95A0280C659A07B30A4E3CA4CF06EC\r\n")
print(uart.read())
uart.write("AT+NWKSKEY=CAD5B1896490A1B402A0BDA6AFD86991\r\n")
print(uart.read()) 
uart.write("AT+ACTIVATE=0\r\n") #ABP Activate
print(uart.read())
uart.write("AT+SAVE\r\n") #ABP Activate
print(uart.read())

cnt = 1
while True:
   print("Packet No #{}".format( cnt ) )
#    temp,pa,hum = bme.values
   temp = bme.temperature
   hum = bme.humidity
   pres = bme.pressure

   vbat = adc.read_core_vbat()      # read MCU VBAT
   print(vbat)
    
   print("********BME280 values:")
   print("temp:",temp," Hum:",hum ,"PA:", pres)
   
   c = CayenneLPP()
   c.addTemperature(1, float(temp)) 
   c.addRelativeHumidity(1, float(hum))
   c.addAnalogInput(1, float(vbat))
   c.addBarometricPressure(1, (float(pres)*100))
   
   d = (ubinascii.hexlify(c.getBuffer()))
   print(" — — — — -Start Send Status — — — — — — ")
   print("AT+NMGS={0},{1}\r\n".format(int(len(d)/2),(d.decode("utf-8"))))
   uart.write("AT+NMGS={0},{1}\r\n".format(int(len(d)/2),(d.decode("utf-8"))))
   #print(uart.read())

#   p = ure.search("0100(.+?)\r\n", uart.read().decode("utf-8"))
   
#   try:
#        print (p.group(0))
#        pgroup=(p.group(0))
#   except AttributeError:
#        pgroup=""
#        print ("Not found Downlink Packet")
        
#   if pgroup=="010001\r\n":
#       print("Command1 Detected: On LED =============>")
#       led.on()
#       time.sleep(0.5)
#   elif pgroup=="010000\r\n":
#       print("Command1 Detected: Off LED =============>")
#       led.off()
#   else:
#       print("No Known Command Detect")
   
#   print("— — — — -End Send Status — — — — — — ")
   cnt = cnt + 1
   #uart.write("AT+SLEEP\r\n") #ABP Activate
   #print(uart.read())
   time.sleep(60.0)
   #machine.deepsleep()