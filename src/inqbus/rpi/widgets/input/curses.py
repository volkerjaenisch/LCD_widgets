import threading

from inqbus.rpi.widgets.base.input import Input
from inqbus.rpi.widgets.events import Input_Down, Input_Up, Input_Click
from inqbus.rpi.widgets.interfaces.widgets import IInput, INotify, IGUI
from zope.component import getUtility
from zope.interface import implementer

try:
    from pigpio_encoder import Rotary
except ImportError:
    from inqbus.rpi.widgets.fake.rotary import Rotary

KEYBOARD_SIGNALS = {
    'u': Input_Up,
    'd': Input_Down,
    'c': Input_Click}


@implementer(IInput)
class InputCurses(Input):

    def __init__(self, curses_display):
        self.display = curses_display

    def run(self):
        thread = threading.Thread(target=self.run_curses)
        thread.start()

    def run_curses(self):
        while True:
            key = self.display.display.getkey()
            if key.lower() in KEYBOARD_SIGNALS:
                signal = KEYBOARD_SIGNALS[key.lower()]
                gui = getUtility(IGUI)
                layout = gui._layout
                notify = INotify(layout.controller)
                notify.notify(signal)

