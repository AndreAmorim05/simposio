from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
from datetime import datetime
from datetime import timedelta



class Manager(ScreenManager):
    pass

class Interface(Screen):
    def __init__(self,**kwargs):
        super(Interface, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

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

class TelaInicial(App):
    def build(self):
        return Manager()
        


if __name__ == '__main__':
    TelaInicial().run()