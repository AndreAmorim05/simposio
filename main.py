from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
from datetime import datetime
from datetime import timedelta
import time

try:
    import Adafruit_ADS1x15
    import Adafruit_DHT
    import RPi.GPIO as GPIO
except:
    pass




class Manager(ScreenManager):
    pass

class Interface(Screen):
    def __init__(self,**kwargs):
        super(Interface, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        try:
            GPIO.setmode(GPIO.BOARD)

            self.adc = Adafruit_ADS1x15.ADS1115()
            self.sensor_DHT11 = Adafruit_DHT.DHT11

            self.values = [0]*4

            self.pino_sensor_DHT11 = 4
            self.GAIN = 1

            self.corrente_eolica = 0
            self.corrente_fotovoltaica = 0
            self.j = 0

            self.umid, self.values[3] = Adafruit_DHT.read_retryself(sensor_DHT11, self.pino_sensor_DHT11)
        except:
            print('Não foi possível identificar o Raspberry Pi')

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
    
    def medicoes(self, *args):
        self.now = self.now + timedelta(seconds = 0.5)
        self.ids.tempo.text = self.now.strftime('%H:%M:%S')

        try:
            for i in range(3):
                self.values[i] = (adc.read_adc(i, gain=self.GAIN) * 4.096) / 32767
                self.values[i] = round(self.values[i], 4)
                
                self.corrente_eolica = self.values[2] / 1000
                self.corrente_fotovoltaica = self.values[2] / 1000
                if j == 10 : 
                    self.umid, self.values[3] = Adafruit_DHT.read_retry(self.sensor_DHT11, self.pino_sensor_DHT11)
                    self.j = 0
                    
                self.j+= 1
                
                self.ids.lb0.text = str(self.values[0])
                self.ids.lb1.text = str(self.values[1])
                self.ids.lb2.text = str(self.values[2])
                self.ids.lb3.text = str(self.values[3])

        except:
            pass

class TelaInicial(App):
    def build(self):
        return Manager()
        


if __name__ == '__main__':
    TelaInicial().run()