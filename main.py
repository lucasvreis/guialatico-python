import os
os.environ['KIVY_SDL2_PATH'] = '~/lib'

import kivy
from kivy.app import App
from kivy.uix.button import Button

from plyer import gps, gravity

import importlib

import nxt.bluesock
from nxt import Motor, Light, Touch, PORT_A, PORT_B, PORT_1, PORT_2
from nxt.brick import Brick

importlib.import_module('request-json')

address = '00:16:53:0E:7E:DE'

class Guialatico(App):
    gps_location = (0,0,0)
    p_bearing = 0
    bearing = 0
    elevation = 0
    some_location = False
    
    nbrick = None
# fazer as tarefas do nxt serem async
    def reset_bearing(self):
        self.motor_a.run(-10, False) #
        self.motor_b.run(10, True) #
        A, B = True, True
        while A or B:
            if self.push_sensor.is_pressed():
                self.motor_a.idle()
                A = False
            if self.color_sensor.get_lightness() > 100:
                self.motor_b.brake()
                B = False
        self.bearing = (self.p_bearing + 90.0) % 360.0
        self.elevation = -70.0 #calibrar

    def on_location(self, **kwargs):
        self.gps_location = (kwargs['lat'], kwargs['lon'], kwargs['altitude'])
        self.bearing = kwargs['bearing']
        self.some_location = True

    def on_connect(self, nxt):
        self.motor_a = Motor(nxt, PORT_A)
        self.motor_b = Motor(nxt, PORT_B)
        self.color_sensor = Light(nxt, PORT_1, True)
        self.push_sensor = Touch(nxt, PORT_2)
        gps.start(10e3, 0)
        print("Waiting for GPS")

    def build(self):
        try:
            gravity.enable()
            compass.enable()
            gps.configure(self.on_location, on_status=None)
        except:
            print("GPS, Compass or Gravity sensors not implemented")
        try:
            nbrick = bluesock.BlueSock(address).connect()
            on_connect(nbrick)
        except:
            print("Cant connect to NXT")
        return Button(text='hello world')


if __name__ == '__main__':
    Guialatico().run()