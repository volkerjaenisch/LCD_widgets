from time import sleep

from inqbus.rpi.widgets.display.curses   import CursesDisplay
from .signals import SIGNAL_UP, SIGNAL_DOWN, SIGNAL_CLICK
from inqbus.rpi.widgets.log import logging

KEYBOARD_SIGNALS = {
    'u' : SIGNAL_UP,
    'd': SIGNAL_DOWN,
    'c': SIGNAL_CLICK,
}


class Controller(object):

    _active_page = None

    @property
    def active_page(self):
        return self._active_page

    @active_page.setter
    def active_page(self, value):
        self._active_page = value
        self._active_page.render()

    def up(self):
        logging.debug('sended signal up')
        self.active_page.notify(SIGNAL_UP)

    def down(self):
        logging.debug('sended signal down')
        self.active_page.notify(SIGNAL_DOWN)

    def click(self):
        logging.debug('sended Signal click')
        self.active_page.notify(SIGNAL_CLICK)

    def register_input(self, input_cls):
        self.input = input_cls(
            self.up,
            self.down,
            self.click,
            )

    def register_display(self, display):
        self.display = display

    def loop(self):
        while True:
            sleep(1)

    def loop_interactive(self):
        while True:
            key = input('Signal u->up, d->down, c->click?')
            signal = KEYBOARD_SIGNALS[key.lower()]
            self.active_page.notify(signal)
            sleep(1)

    def loop_curses(self, display=None):
        if not display:
            display = CursesDisplay()
        while True:
            key = display.display.getkey()
            if key.lower() in KEYBOARD_SIGNALS:
                signal = KEYBOARD_SIGNALS[key.lower()]
                self.active_page.notify(signal)

