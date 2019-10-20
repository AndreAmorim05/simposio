from kivy.app import App
from datetime import datetime
from datetime import timedelta
from kivy.clock import Clock
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        self.now = datetime.now().replace(hour=0,minute=0,second=0)
        

        # Schedule the self.update_clock function to be called once a second
        Clock.schedule_interval(self.update_clock, 1)
        self.my_label = Label(text= self.now.strftime('%H:%M:%S'))
        return self.my_label  # The label is the only widget in the interface

    def update_clock(self, *args):
        # Called once a second using the kivy.clock module
        # Add one second to the current time and display it on the label
        self.now = self.now + timedelta(seconds = 1)
        self.my_label.text = self.now.strftime('%H:%M:%S')

MyApp().run()





# import kivy
# kivy.require('1.0.6') # replace with your current kivy version !

# import datetime

# from kivy.app import App
# from kivy.clock import Clock
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.uix.image import Image
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.gridlayout import GridLayout

# now = datetime.datetime.now() - datetime.datetime.now()
# print(now)






