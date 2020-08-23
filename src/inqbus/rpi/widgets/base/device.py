from zope.interface import implementer

from inqbus.rpi.widgets.interfaces.interfaces import IDevice


@implementer(IDevice)
class Device(object):

    is_init = False

    def init(self):
        self.is_init = True

    def run(self):
        pass

    def done(self):
        pass
