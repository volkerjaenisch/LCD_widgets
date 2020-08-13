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
        self.rotary = Rotary(clk=17, dt=22, sw=27)
        self.rotary.setup_rotary(rotary_callback=self.rotary_callback)
        self.rotary.setup_switch(sw_short_callback=self.click_callback)
        gui = getUtility(IGUI)
        layout = gui._layout
        self.notify = INotify(layout.controller)

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
