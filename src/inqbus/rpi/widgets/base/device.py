from zope.interface import implementer

from src.inqbus.rpi.widgets.interfaces.widgets import IDevice


@implementer(IDevice)
class Device(object):

    def init(self):
        pass

    def run(self):
        pass

    def done(self):
        pass
