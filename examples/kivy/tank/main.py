import time
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.animation import Animation
from kivy.lang import Builder

import nxt.motor

from common.brickfinder import popup_finder

class CenteringSlider(Slider):
    """center automatically if released"""
    def on_touch_up(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            Animation(value=0,duration=.2,t='out_back').start(self)

class TankWidget(BoxLayout):
    def __init__(self,**kwargs):
        self.brick = None
        super(TankWidget, self).__init__(**kwargs)

    def start_tank(self,dt):
        self._motleft = nxt.motor.Motor(self.brick, nxt.motor.PORT_B)
        self._motright = nxt.motor.Motor(self.brick, nxt.motor.PORT_C)
        Clock.schedule_interval(self.update_motors, 0.1)

    def update_motors(self,dt):
        start = time.time()
        is_regulated = self.ids.regulate_check.active
        self._motleft.run(power=self.ids.left_slider.value,regulated=is_regulated)
        self._motright.run(power=self.ids.right_slider.value,regulated=is_regulated)
        interval = time.time()-start
        print('updated in:{:.03}'.format(interval))


Builder.load_string("""
<TankController@CenteringSlider>:
    min:-127
    max:127
    value:0
    orientation: 'vertical'

<TankWidget>:
    orientation: 'vertical'
    FloatLayout:
        orientation: 'horizontal'
        size_hint_y: 0.2
        Label:
            text: "Regulate Speed:"
            pos_hint: {'x':0,'y':0}
        CheckBox:
            id:regulate_check
            pos_hint: {'x':0.2,'y':0}
            active: True
    BoxLayout:
        orientation: 'horizontal'
        padding: 0,30,0,30
        TankController:
            id:left_slider
        TankController:
            id:right_slider
""")


class TankApp(App):
    def build(self):
        self._tank = TankWidget()
        return self._tank

    def on_start(self):
        pass
        popup_finder(self.brickfound_callback)

    def brickfound_callback(self, brick):
        if brick:
            print('we found it :-)')
            self._tank.brick = brick
            Clock.schedule_once(self._tank.start_tank,1.0)
        else:
            print('no brick :-(')
            self.stop()


if __name__ == '__main__':
    TankApp().run()