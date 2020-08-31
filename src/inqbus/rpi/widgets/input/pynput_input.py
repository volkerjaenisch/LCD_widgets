from time import sleep

from inqbus.rpi.widgets.base.input import BlockingInput
from inqbus.rpi.widgets.base.signals import InputChar
from inqbus.rpi.widgets.input.signals import KEYBOARD_SIGNALS
from inqbus.rpi.widgets.interfaces.input import IBlockingInput
from pynput import keyboard
from zope.interface import implementer


@implementer(IBlockingInput)
class PynputInput(BlockingInput):
    """
    Input from the keyboard via the pynput python lib.
    """
    def __init__(self, keyboard_signals=None):
        """
        A dict of keyboard to signal mappings
        can be given to the PynputInput instance
        :param keyboard_signals: A dict of keyboard to signal mappings
        """
        if keyboard_signals:
            self.keyboard_signals = keyboard_signals
        else:
            self.keyboard_signals = KEYBOARD_SIGNALS

    def init(self):
        """
        :return:
        """
        pass

    def run(self, queue):
        """
        Setup the queue for thread safe communiation with the GUI
        :param queue: communiation queue. Will be set by the frameworks
                run method if the input is blocking.
        :return:
        """
        super(PynputInput, self).run(queue)
        # Configure a handler for key release events
        self.listener = keyboard.Listener(
            on_release=self.on_key_release)
        # Start the listener
        self.listener.start()

    def on_key_release(self, key):
        """
        Handler for key_release events.
        :param key:
        :return:
        """
        # get the current released key as its character
        char = key.char.lower()
        # if the key is registered for a signal ..
        if char in self.keyboard_signals:
            # .. optain the signal
            signal = self.keyboard_signals[char]
        else:
            # if not generate a Character input signal containing the character
            signal = InputChar(char)
        # finally send the signal to the queue
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
