from inqbus.rpi.widgets.base.input import Input
from inqbus.rpi.widgets.signals import Input_Down, Input_Up, Input_Click
from inqbus.rpi.widgets.interfaces.widgets import IInput, IGUI, INotify
from zope.component import getUtility
from zope.interface import implementer

try:
    from pigpio_encoder import Rotary
except ImportError:
    from inqbus.rpi.widgets.fake.rotary import Rotary


@implementer(IInput)
class RotaryInput(Input):

    rotary = None
    counter = None

    def __init__(self):
        self.rotary = Rotary(clk_gpio=22, dt_gpio=27, sw_gpio=17)
        self.rotary.setup_rotary(min=0, max=50, rotary_callback=self.rotary_callback)
        self.rotary.setup_switch(sw_short_callback=self.click_callback)
        self.rotary.counter = 25

    def init(self):
        gui = getUtility(IGUI)
        focus = gui.focus
        self.notify = INotify(focus.controller)

    def run(self):
        pass


    def rotary_callback(self, counter):
        print('Rotation', counter)
        if not self.counter:
            self.counter = counter
            return
        if counter > self.counter:
            self.counter = counter
            self.notify.notify(Input_Up)
        elif counter < self.counter:
            self.counter = counter
            self.notify.notify(Input_Down)

    def click_callback(self):
        print('Click!')
        self.notify.notify(Input_Click)
