
from pigpio_encoder import Rotary
from src.base.input import Input


class InputRotary(Input):

    rotary = None
    counter = None

    def __init__(self, up_handler, down_handler, click_handler):
        self.up_handler = up_handler
        self.down_handler = down_handler
        self.click_handler = click_handler
        self.rotary = Rotary(clk=17, dt=22, sw=27)
        self.rotary.setup_rotary(rotary_callback=self.rotary_callback)
        self.rotary.setup_switch(sw_short_callback=self.click_callback)

    def rotary_callback(self, counter):
        print('Rotation', counter)
        if not self.counter:
            self.counter = counter
            return
        if counter > self.counter:
            self.counter = counter
            self.up_handler()
        elif counter < self.counter:
            self.counter = counter
            self.down_handler()

    def click_callback(self):
        print('Click!')
        self.click_handler()
