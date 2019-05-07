import os
os.environ['KIVY_SDL2_PATH'] = '~/lib'
import kivy
from kivy.app import App
from kivy.uix.button import Button
from plyer import gps, gravity
import importlib
importlib.import_module('request-json')

class Guialatico(App):
    gps_location = (0,0,0)
    bearing = 0
    def on_location(self, **kwargs):
        self.gps_location = (kwargs['lat'], kwargs['lon'], kwargs['altitude'])
        self.bearing = kwargs['bearing']

    def build(self):
        try:
            gravity.enable()
            compass.enable()
            gps.configure(self.on_location, on_status=None)
        except:
            print("GPS, Compass or Gravity sensors not implemented")
        return Button(text='hello world')


if __name__ == '__main__':
    Guialatico().run()