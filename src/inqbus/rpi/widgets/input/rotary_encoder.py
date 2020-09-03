
from inqbus.rpi.widgets.base.input import Input
from inqbus.rpi.widgets.base.log import logging
from inqbus.rpi.widgets.base.signals import InputClick, InputDown, InputUp
from inqbus.rpi.widgets.interfaces.input import IInput
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
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
        Initialize the rotary encoder.
        A rotary encoder instance may be given to this method
        if not an encoder instance is created.

        Args:
            rotary (:obj:`pigpio_encoder.Rotary`, optional)
        """
        if not rotary:
            self.rotary = self.get_rotary()
        else:
            self.rotary = rotary

        # Remember the current counter value of the rotary
        self.counter = self.rotary.counter
        # get us a link to the GUI to dispatch it of signals
        gui = getUtility(IGUI)
        self.gui = gui
        # set us to initialized state
        self.initialized = True

    def get_rotary(self):
        """
        Create a rotary encoder instance.
        Can be overridden by you.
        But keep in mind to register the correct callbacks.

        Returns:
            The rotary encoder instance
        """
        rotary = Rotary(clk_gpio=22, dt_gpio=27, sw_gpio=17)
        rotary.setup_rotary(
                min=0,
                max=50,
                rotary_callback=self.rotary_callback
        )
        rotary.setup_switch(sw_short_callback=self.click_callback)
        rotary.counter = 25
        return rotary

    def run(self):
        pass

    def rotary_callback(self, counter):
        """
        Call back for rotation. Dispatches Up/Down-Signals.

        Args:
            counter: The new counter value from the rotary driver

        """

        logging.debug('Rotation %s', counter)
        # check if we are initialized ..
        if not self.initialized:
            # .. if not return
            return
        # if the counter from the rotary is larger than the memoized counter ..
        if counter > self.counter:
            # .. memoize the new  counter value
            self.counter = counter
            # and dispatch the gui of an InputUp Signal
            self.gui.dispatch(InputUp)
        # if the counter from the rotary is smaller than
        # the memorized counter ..
        elif counter < self.counter:
            # .. memoize the new  counter value
            self.counter = counter
            self.gui.dispatch(InputDown)
            # and dispatch the gui of an InputDown Signal

    def click_callback(self):
        """
        Call back for click operation. Dispatches Click-Signals.
        """
        logging.debug('Click!')
        # check if we are initialized ..
        if not self.initialized:
            return
        # and dispatch the gui of an InputClick Signal
        self.gui.dispatch(InputClick)
