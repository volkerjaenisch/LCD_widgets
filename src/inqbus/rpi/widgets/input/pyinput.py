from inqbus.rpi.widgets.base.input import Input
from inqbus.rpi.widgets.input.signals import KEYBOARD_SIGNALS
from inqbus.rpi.widgets.interfaces.widgets import IInput, INotify, IGUI
from pynput import keyboard
from zope.component import getUtility
from zope.interface import implementer


@implementer(IInput)
class Pynput(Input):

    def on_press(key):
        pass

    def run(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_key_release)
        listener.start()

    def on_key_release(key):
        if key.lower() in KEYBOARD_SIGNALS:
            signal = KEYBOARD_SIGNALS[key.lower()]
            gui = getUtility(IGUI)
            layout = gui._layout
            notify = INotify(layout.controller)
            notify.notify(signal)
