from inqbus.rpi.widgets.interfaces.widgets import IInput, IGUI
from zope.component import getUtility
from zope.interface import implementer




@implementer(IInput)
class Input(object):
    up_handler = None
    down_handler = None
    click_handler = None
    target = None

    def init(self, target):
        self.target = target

    def run(self):
        pass

    def done(self):
        pass
