import threading
from time import sleep

from inqbus.rpi.widgets.interfaces.display import IDisplay
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.visibility import IBlinking
from inqbus.rpi.widgets.interfaces.widgets import IWidget
from zope.component import getGlobalSiteManager, getMultiAdapter
from zope.interface import implementer


@implementer(IBlinking)
class Blinking(object):
    __used_for__ = (IWidget, IDisplay)

    def __init__(self, widget, display):
        self.widget = widget
        self.display = display

    def __call__(self):
        self.thread = threading.Thread(target=self.blink)
        self.thread.start()

    def blink(self):
        renderer = getMultiAdapter((self.widget, self.display), interface=IRenderer)
        while True:
            if not self.display.is_init:
                sleep(0.5)
                continue
            renderer.render()
            sleep(0.5)
            renderer.clear()
            sleep(0.5)


gsm = getGlobalSiteManager()
gsm.registerAdapter(Blinking, (IWidget, IDisplay), IBlinking)
