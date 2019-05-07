__author__ = 'rupello'

import threading

from kivy.uix.rst import RstDocument
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import nxt

try:
    from jnius import detach
except:
    def detach():
        pass


class LogDisplayWidget(RstDocument):
    def __init__(self, title='',**kwargs):
        self._logbuffer = [title,
                           '='*len(title),
                           '::',
                           '']
        Clock.schedule_interval(self.update_displayed_text, 0.5)
        super(LogDisplayWidget, self).__init__(**kwargs)

    def update_displayed_text(self,dt):
        self.text = '\n'.join(self._logbuffer)
        self.scroll_y = 0  # scroll to bottom

    def log(self,message):
        """lod a message to the console and gui"""
        print(message)
        self._logbuffer.append(message)


class BrickFinder(object):
    """find the brick on a background thread"""
    def __init__(self):
        self.brick = None

    def start(self):
        self._connect_thread = threading.Thread(target=self._run_find_brick)
        self._connect_thread.start()

    def _run_find_brick(self):
        try:
            self.brick = nxt.find_one_brick(debug=True)
        finally:
            # kivy/android will crash here if we don't detach
            print('detaching thread')
            detach()

    def searching(self):
        self._connect_thread.join(timeout=0.1)
        return self._connect_thread.isAlive()


class BrickFinderWidget(LogDisplayWidget):
    """
       A Widget that shows search progress and support s property
    """

    def __init__(self,title='Connecting to Brick...',start=False,**kwargs):
        self._bf = BrickFinder()
        self.register_event_type('on_search_complete')
        if start:
            self.start()
        super(BrickFinderWidget, self).__init__(title,**kwargs)

    def start(self):
        self._bf.start()
        Clock.schedule_once(self.check_brick_connection, 1.5)

    def check_brick_connection(self,dt):
        """wait for find_brick thread to complete, then print info"""
        self.log(' Searching for a brick...')
        if self._bf.searching():
            # check back later
            Clock.schedule_once(self.check_brick_connection,1.5)
        else:
            if self._bf.brick:
                self.brick = self._bf.brick # notify observers
                self.log(' brick found :-)')
                info = self._bf.brick.get_device_info()
                self.log(' Name:{}'.format(info[0].strip('\x00')))
                self.log(' Address:{}'.format(info[1]))
                self.log(' Firmware:{}'.format(self._bf.brick.get_firmware_version()))
                self.log(' Battery:{}mV'.format(self._bf.brick.get_battery_level()))
            else:
                self.log(' brick not found :-(')
                self.log(' Check brick is powered on and paired.')
            # notify observers
            self.dispatch('on_search_complete', self._bf.brick)

    def on_search_complete(self, *args):
        pass

class BrickFinderDialogWidget(BoxLayout):
    def __init__(self,**kwargs):
        super(BrickFinderDialogWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self._bfw = BrickFinderWidget(start=True)
        self.add_widget(self._bfw)
        self._bfw.bind(on_search_complete=self.on_search_complete)
        self.btnOK = Button(text='OK',size_hint=(1, .2),disabled=True)
        self.add_widget(self.btnOK)

    def on_search_complete(self,instance,brick):
        self._bf = instance
        self._brick = brick
        self.btnOK.disabled = False



def popup_finder(callback):
    """show the finder in a popup, calling <callback> on completion"""
    bfdw = BrickFinderDialogWidget()
    popup = Popup(title='', content=bfdw,
                  auto_dismiss=False,
                  size_hint=(0.6,0.8))
    bfdw.btnOK.bind(on_press=popup.dismiss)
    bfdw.btnOK.bind(on_press=lambda x: callback(bfdw._brick))
    popup.open()
