
from inqbus.rpi.widgets.base.log import logging

from inqbus.rpi.widgets.base.input import Input
from inqbus.rpi.widgets.base.signals import Input_Down, Input_Up, Input_Click
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from inqbus.rpi.widgets.interfaces.input import IInput
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
    initialized = False

    def init(self, rotary=None):
        """
        Initialize the rotary encoder. A rotary encoder instance may be given to this method.
        If not a encoder instance is created.
        :param rotary:
        :return:
        """
        if not rotary:
            self.rotary = self.get_rotary()
        else:
            self.rotary = rotary

        # Remember the current counter value of the rotary
        self.counter = self.rotary.counter
        # get us a link to the GUI to notify it of signals
        gui = getUtility(IGUI)
        self.gui = gui
        # set us to initialized state
        self.initialized = True

    def get_rotary(self):
        """
        Create a rotary encoder instance. Can be overridden by you. But keep in mind to register the correct
        callbacks.
        :return:
        """
        rotary = Rotary(clk_gpio=22, dt_gpio=27, sw_gpio=17)
        rotary.setup_rotary(min=0, max=50, rotary_callback=self.rotary_callback)
        rotary.setup_switch(sw_short_callback=self.click_callback)
        rotary.counter = 25
        return rotary

    def run(self):
        pass

    def rotary_callback(self, counter):
        """Call back for rotation"""
        logging.debug('Rotation %s', counter)
        # check if we are initialized ..
        if not self.initialized:
            # .. if not return
            return
        # if the counter from the rotary is larger than the memoized counter ..
        if counter > self.counter:
            # .. memoize the new  counter value
            self.counter = counter
            # and notify the gui of an Input_Up Signal
            self.gui.notify(Input_Up)
        # if the counter from the rotary is smaller than the memoized counter ..
        elif counter < self.counter:
            # .. memoize the new  counter value
            self.counter = counter
            self.gui.notify(Input_Down)
            # and notify the gui of an Input_Down Signal

    def click_callback(self):
        """
        Call back for cklick operation
        :return:
        """
        logging.debug('Click!')
        # check if we are initialized ..
        if not self.initialized:
            return
        # and notify the gui of an Input_Click Signal
        self.gui.notify(Input_Click)
