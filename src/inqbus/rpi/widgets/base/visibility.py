import threading
from queue import Queue, Empty

from time import sleep

from inqbus.rpi.widgets.interfaces.display import IDisplay
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.visibility import IBlinking, IScrolling
from inqbus.rpi.widgets.interfaces.widgets import IWidget
from zope.component import getGlobalSiteManager, getMultiAdapter
from zope.interface import implementer


@implementer(IBlinking)
class Blinking(object):
    __used_for__ = (IWidget, IDisplay)

    def __init__(self, widget, display):
        self.widget = widget
        self.display = display
        self.is_break = False
        self.queue = Queue()

    def __call__(self):
        self.thread = threading.Thread(target=self.blink, args =(self.queue, ))
        self.thread.start()

    def blink(self, queue):
        renderer = getMultiAdapter((self.widget, self.display), interface=IRenderer)
        while True:
            if not self.display.is_init:
                sleep(0.5)
                continue
            renderer.render()
            try:
                signal = queue.get(block=False)
                break
            except Empty:
                pass
            sleep(0.5)
            renderer.clear()
            sleep(0.5)

    def done(self):
        self.queue.put(True)


gsm = getGlobalSiteManager()
gsm.registerAdapter(Blinking, (IWidget, IDisplay), IBlinking)


@implementer(IScrolling)
class Scrolling(object):
    __used_for__ = (IWidget, IDisplay)

    def __init__(self, widget, display):
        self.widget = widget
        self.display = display

    def __call__(self):
        self.thread = threading.Thread(target=self.scroll)
        self.thread.start()

    def scroll(self):
        renderer = getMultiAdapter((self.widget, self.display), interface=IRenderer)
        while True:
            if not self.display.is_init:
                sleep(0.5)
                continue
            else:
                break
        while True:
            for i in range(self.widget.length):
                renderer.clear()
                sleep(0.5)
                self.widget.scroll_pos = i
                renderer.render()
                sleep(0.5)


gsm = getGlobalSiteManager()
gsm.registerAdapter(Scrolling, (IWidget, IDisplay), IScrolling)
