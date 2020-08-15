import curses
import threading

from inqbus.rpi.widgets.base.input import Input

from inqbus.rpi.widgets.interfaces.widgets import IInput, INotify, IGUI
from zope.component import getUtility
from zope.interface import implementer

try:
    from pigpio_encoder import Rotary
except ImportError:
    from inqbus.rpi.widgets.fake.rotary import Rotary



@implementer(IInput)
class InputCurses(Input):

    def __init__(self, curses_display):

        if not curses_display:
            self.display =  curses.newwin(1, 1, 0, 0)
        else:
            self.display = curses_display.display

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
                notify = INotify(layout.controller)
                notify.notify(signal)

