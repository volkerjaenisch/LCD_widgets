import curses
import threading

from inqbus.rpi.widgets.base.input import Input

from inqbus.rpi.widgets.interfaces.interfaces import INotify, IGUI
from inqbus.rpi.widgets.interfaces.input import IInput
from zope.component import getUtility
from zope.interface import implementer

try:
    from pigpio_encoder import Rotary
except ImportError:
    from inqbus.rpi.widgets.fake.rotary import Rotary



@implementer(IInput)
class InputCurses(Input):
    """
    Input from a curses frame_buffer. CURRENTLY NOT WORKING!
    """

    def __init__(self, curses_display):

        if not curses_display:
            self.display =  curses.newwin(1, 1, 0, 0)
        else:
            self.display = curses_display.frame_buffer

    def run(self):
        thread = threading.Thread(target=self.run_curses)
        thread.start()

    def run_curses(self):
        while True:
            key = self.display.getkey()
            if key.lower() in KEYBOARD_SIGNALS:
                signal = KEYBOARD_SIGNALS[key.lower()]
                gui = getUtility(IGUI)
                layout = gui._layout
                layout.controller.notify(signal)

