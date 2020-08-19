from inqbus.rpi.widgets.interfaces.interfaces import IDevice
from zope.interface import Attribute


class IInput(IDevice):
    pass


class IBlockingInput(IInput):
    queue = Attribute("""Synced-Queue to main thread""")

    def run(self, queue):
        pass
