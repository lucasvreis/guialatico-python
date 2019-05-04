from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

try:
    from jnius import autoclass
    Hardware = autoclass('org.renpy.android.Hardware')
except:
    Hardware = None

import nxt.motor

from common.brickfinder import popup_finder

class SegwayWidget(BoxLayout):
    def __init__(self,**kwargs):
        self.brick = None
        super(SegwayWidget, self).__init__(**kwargs)

    def start(self,dt):
        if Hardware:
            Hardware.orientationSensorEnable(True)
        Clock.schedule_interval(self.update, 0.1)

    def update(self,dt):
        az,el,rot = [0.,0.,0.]
        if Hardware:
            az,el,rot = Hardware.orientationSensorReading()
        self.ids.orient_axis_0_label.text = 'Az: {:07.3f}'.format(az)
        self.ids.orient_axis_1_label.text = 'El: {:07.3f}'.format(el)
        self.ids.orient_axis_2_label.text = 'Ro: {:07.3f}'.format(rot)

        # 0 to 360 (azimuth)
        self.ids.orient_axis_0_bar.value = int(100.*az/360.)

        # -180 to +180 (elevation)
        self.ids.orient_axis_1_bar.value = int(100.*(el+180.)/360.0)

        # -90 to +90
        self.ids.orient_axis_2_bar.value = int(100.*(rot+90.)/180.)
        print(az,el,rot)

    def stop(self,dt):
        if Hardware:
            Hardware.orientationSensorEnable(False)

Builder.load_string("""
<OrientLabel@Label>
    halign: 'left'
    size_hint_x: 1.
    text_size: self.size

<OrientBar@ProgressBar>
    value: 0
    min: 0
    max: 100

<SegwayWidget>:
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        BoxLayout:
            orientation: 'vertical'
            OrientLabel:
                id: orient_axis_0_label
                text: 'Axis 0:'
            OrientBar:
                id: orient_axis_0_bar
        BoxLayout:
            orientation: 'vertical'
            OrientLabel:
                id: orient_axis_1_label
                text: 'Axis 1:'
            OrientBar:
                id: orient_axis_1_bar
        BoxLayout:
            orientation: 'vertical'
            OrientLabel:
                id: orient_axis_2_label
                text: 'Axis 2:'
            OrientBar:
                id: orient_axis_2_bar
""")


class SegwayApp(App):
    def build(self):
        self._segway = SegwayWidget()
        return self._segway

    def on_start(self):
        #popup_finder(self.brickfound_callback)
        Clock.schedule_once(self._segway.start,0.)

    def brickfound_callback(self, brick):
        if brick:
            print('we found it :-)')
            self._tank.brick = brick
            Clock.schedule_once(self._segway.start,0.)
        else:
            print('no brick :-(')
            self.stop()

    def on_stop(self):
        self._segway.stop()


if __name__ == '__main__':
    SegwayApp().run()