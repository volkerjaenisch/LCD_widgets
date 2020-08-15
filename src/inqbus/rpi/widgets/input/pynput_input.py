from time import sleep

from inqbus.rpi.widgets.base.input import Input, BlockingInput
from inqbus.rpi.widgets.input.signals import KEYBOARD_SIGNALS
from inqbus.rpi.widgets.interfaces.widgets import IBlockingInput
from pynput import keyboard
from zope.interface import implementer


@implementer(IBlockingInput)
class PynputInput(BlockingInput):

    def init(self):
        pass

    def run(self, queue):
        super(PynputInput, self).run(queue)

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
