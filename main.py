import os
os.environ['KIVY_SDL2_PATH'] = '~/lib'
import kivy
from kivy.app import App
from common.brickfinder import BrickFinderWidget
class InfoApp(App):
    def build(self):
        bfw = BrickFinderWidget(title='NXT Demo',start=True)
        bfw.bind(on_search_complete=self.brickfound_callback)
        return bfw

    def brickfound_callback(self, finder_widget, brick):
        if brick:
            print('we found it :-)')
        else:
            print('no brick :-(')


if __name__ == '__main__':
    InfoApp().run()