from zope.interface import implementer

from inqbus.rpi.widgets.interfaces.interfaces import IDevice


@implementer(IDevice)
class Device(object):

    def init(self):
        pass

    def run(self):
        pass

    def done(self):
        pass
