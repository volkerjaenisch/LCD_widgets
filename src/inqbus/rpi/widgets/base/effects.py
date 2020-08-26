"""
Adapters for visual effects on widgets. E.G. blinking, scrolling
"""

import threading
from queue import Queue, Empty

from time import sleep

from inqbus.rpi.widgets.interfaces.display import IDisplay
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.effects import IBlinking, IScrolling
from inqbus.rpi.widgets.interfaces.widgets import IWidget
from zope.component import getGlobalSiteManager, getMultiAdapter
from zope.interface import implementer


@implementer(IBlinking)
class Blinking(object):
    """
    Adapter for blinking widgets. This adapter starts its own thread to render the widget on/off
    """
    __used_for__ = (IWidget, IDisplay)

    def __init__(self, widget, display):
        self.widget = widget
        self.display = display
        # Signal Queue to control the blinking thread
        self.queue = Queue()

    def __call__(self, blink_delay=0.5):
        self.blink_delay = blink_delay
        # Start the blinking thread
        self.thread = threading.Thread(target=self.blink, args =(self.queue, ))
        self.thread.start()

    def blink(self, queue):
        """
        Do the blinking by renderen/clearing the widget at the blink_delay schedule.
        :param queue: Signal queue for interrupting the blink thread
        :return: None
        """
        # get the renderer for the widget/display
        renderer = getMultiAdapter((self.widget, self.display), interface=IRenderer)
        while True:
            # Not initilized yet?
            if not self.display.is_init:
                sleep(self.blink_delay)
                continue
            # Render the widget. This is important to prevent an empty widget when blinking stops
            renderer.render()
            # check for stopping the blinking
            try:
                # get a signla from the queue
                signal = queue.get(block=False)
                # if we got a signal break the loop/end the thread
                break
            # if the queue is empty we have to continue
            except Empty:
                pass
            sleep(self.blink_delay)
            renderer.clear()
            sleep(self.blink_delay)

    def done(self):
        """
        Halt the blinking
        :return: None
        """
        self.queue.put(True)


gsm = getGlobalSiteManager()
gsm.registerAdapter(Blinking, (IWidget, IDisplay), IBlinking)


@implementer(IScrolling)
class Scrolling(object):
    """
    Adapter for scrolling widgets
    """
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
