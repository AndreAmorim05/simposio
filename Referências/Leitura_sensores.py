import time
import Adafruit_ADS1x15
import Adafruit_DHT
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

adc = Adafruit_ADS1x15.ADS1115()
sensor_DHT11 = Adafruit_DHT.DHT11

values = [0]*4

pino_sensor_DHT11 = 4
GAIN = 1

corrente_eolica = 0
corrente_fotovoltaica = 0
j = 0

umid, values[3] = Adafruit_DHT.read_retry(sensor_DHT11, pino_sensor_DHT11)

while True:
    
    for i in range(3):
        values[i] = (adc.read_adc(i, gain=GAIN) * 4.096) / 32767
        values[i] = round(values[i], 4)
        
    corrente_eolica = values[2] / 1000
    corrente_fotovoltaica = values[2] / 1000
    if j == 10 : 
        umid, values[3] = Adafruit_DHT.read_retry(sensor_DHT11, pino_sensor_DHT11)
        j = 0
        
    time.sleep(0.5)
    j+= 1
    print(values)
