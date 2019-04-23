import random

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window


Window.size = (640, 380)



class Test(TabbedPanel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.random_number = str(random.randint(1, 100))
        self.cmd_log.text = self.random_number

    def change_text(self, event):
        self.random_number = str(random.randint(1, 100))
        self.cmd_log.text = self.random_number
    pass


class testApp(App):
    def build(self):
        return Test()


testApp().run()