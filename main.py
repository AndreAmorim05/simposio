from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
from datetime import datetime
from datetime import timedelta
import time
from math import sin

try:
    import Adafruit_ADS1x15
    import Adafruit_DHT
    import RPi.GPIO as GPIO
except:
    print("Bibliotecas nao foram importadas")
    



class Manager(ScreenManager):
    pass

class Interface(Screen):
    def __init__(self,**kwargs):
        super(Interface, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.value = 0
        try:
            
            GPIO.setmode(GPIO.BOARD)
            try:
                GPIO.setup(25, GPIO.OUT)
            except:
                print ("Porta GPIO 25 nao configurada")
            self.adc = Adafruit_ADS1x15.ADS1115()
            self.sensor_DHT11 = Adafruit_DHT.DHT11

            self.values = [0]*4
            self.pino_sensor_DHT11 = 4
            self.GAIN = 1

            self.corrente_eolica = 0
            self.corrente_fotovoltaica = 0
            self.j = 0

            self.umid, self.values[3] = Adafruit_DHT.read_retry(self.sensor_DHT11, self.pino_sensor_DHT11)
        except:
            print('Nao foi possivel identificar o Raspberry Pi')

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'enter':
            try:
                self.now = datetime.now().replace(hour=0,minute=0,second=0)
                self.event = Clock.schedule_interval(self.medicoes, 0.5)
            except:
                pass
        elif keycode[1] == 'p':
            try:
                self.event.cancel()
            except:
                pass

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def medicoes(self, tempo):
        self.now = self.now + timedelta(seconds = 0.5)
        self.ids.tempo.text = self.now.strftime('%H:%M:%S')

        try:
            for i in range(3):
                self.values[i] = (self.adc.read_adc(i, gain=self.GAIN) * 4.096) / 32767
                self.values[i] = round(self.values[i], 4)
                
            self.corrente_eolica = self.values[1] / 1000
            self.corrente_fotovoltaica = self.values[2] / 1000
            
            if self.j == 10 : 
                self.umid, self.values[3] = Adafruit_DHT.read_retry(self.sensor_DHT11, self.pino_sensor_DHT11)
                self.j = 0
                    
            self.j+= 1
                
            self.ids.lb0.text = str(round(self.values[0],2))
            self.ids.lb1.text = str(round(self.corrente_eolica,2))
            self.ids.lb2.text = str(round(self.corrente_fotovoltaica,2))
            self.ids.lb3.text = str(round(self.values[3],2))

            if self.value*100 <= 100:
                self.value += sin(tempo*0.0015)
                self.ids.pgb.value = abs(100*self.value)
                self.ids.percent.text = str(round(100*self.value,1))+'%'
            else:
                self.ids.percent.text = '100.0%'
                
            
        except:
            if self.value*100 <= 100:
                self.value += sin(tempo*0.0015)
                self.ids.pgb.value = abs(100*self.value)
                self.ids.percent.text = str(round(100*self.value,1))+'%'
            else:
                self.ids.percent.text = '100.0%'
            print("Erro na leitura")
            pass


    def motor(self, active):
        if active == False:
            print('Ligou', active)
            self.event2 = Clock.schedule_interval(self.descarga, 0.5)
            try:
                GPIO.output(25,GPIO.HIGH)
            except:
                pass
        else:
            print('Desligou')

            try:
                self.event2.cancel()
                GPIO.output(25,GPIO.LOW)
            except:
                pass

    def descarga(self, t):
        if self.value*100 > 0:
            self.value -= sin(t*0.005)
        else:
            self.value = 0.000
            try:
                GPIO.output(25,GPIO.LOW)
            except:
                pass

class TelaInicial(App):
    def build(self):
        return Manager()
        


if __name__ == '__main__':
    TelaInicial().run()
