from inqbus.rpi.widgets.base.device import Device
from inqbus.rpi.widgets.interfaces.input import IInput, IBlockingInput
from zope.interface import implementer


@implementer(IInput)
class Input(Device):
    """
    Base of all input devices
    """
    pass

@implementer(IBlockingInput)
class BlockingInput(Input):
    """
    Base of all Blocking input devices. A blocking device has to use a signal queue to communicate for its
    thread with the mainthread.
    """
    queue = None

    def run(self, queue):
        """
        The run function will be called from the GUI with the signal queue.
        :param queue:
        :return:
        """
        self.queue = queue


