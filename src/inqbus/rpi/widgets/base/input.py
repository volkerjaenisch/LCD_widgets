from inqbus.rpi.widgets.base.device import Device
from inqbus.rpi.widgets.interfaces.widgets import (
    IInput, IBlockingInput, )
from zope.interface import implementer


@implementer(IInput)
class Input(Device):
    up_handler = None
    down_handler = None
    click_handler = None
    target = None


@implementer(IBlockingInput)
class BlockingInput(Input):
    queue = None

    def run(self, queue):
        self.queue = queue


