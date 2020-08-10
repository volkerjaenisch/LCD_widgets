from inqbus.rpi.widgets.input.signals import KEYBOARD_SIGNALS
from inqbus.rpi.widgets.interfaces.widgets import IInput, IGUI, INotify
from zope.component import getUtility
from zope.interface import implementer




@implementer(IInput)
class Input(object):
    up_handler = None
    down_handler = None
    click_handler = None
    target = None

    def init(self):
        pass

    def run(self):
        pass

    def done(self):
        pass



