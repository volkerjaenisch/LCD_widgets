from time import sleep

from inqbus.rpi.widgets.base.input import Input
from inqbus.rpi.widgets.input.signals import KEYBOARD_SIGNALS
from inqbus.rpi.widgets.interfaces.widgets import IInput, INotify, IGUI
from pynput import keyboard
from zope.component import getUtility
from zope.interface import implementer


@implementer(IInput)
class PynputInput(Input):

    def run(self, queue):
        self.queue = queue
        self.listener = keyboard.Listener(
            on_release=self.on_key_release)
        self.listener.start()

    def on_key_release(self, key):
        char = key.char.lower()
        if char in KEYBOARD_SIGNALS:
            signal = KEYBOARD_SIGNALS[char]
            self.queue.put(signal)

def test(key):
    print('Released: ' + key)

def main():
    listener = keyboard.Listener(
            on_release=test)
    listener.start()
    while True:
        sleep(1)

if __name__ == '__main__':
    main()
