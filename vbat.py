import pyb

#adc = pyb.ADC(17)              # create an analog object from a pin
#val = adc.read()                # read an analog value
#print(val)
adc = pyb.ADCAll(12)    # create an ADCAll object
#val = adc.read_channel(17) # read the given channel
#print(val)
val = adc.read_core_temp()      # read MCU temperature
print(val)
val = adc.read_core_vbat()      # read MCU VBAT
print(val)
val = adc.read_core_vref()
print(val)

#while True:

  #print()

  #sleep(5)
