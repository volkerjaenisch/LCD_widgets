from zope.interface import implementer

from inqbus.rpi.widgets.interfaces.interfaces import IDevice


@implementer(IDevice)
class Device(object):
    """
    A device is the abstraction of a hardware device. Such a Device has to be :
    * initialized (init)
    * used (run)
    * and its resources freed in the end (done)
    """

    # Am I initialized
    is_init = False

    def init(self):
        self.is_init = True

    def run(self):
        pass

    def done(self):
        pass
