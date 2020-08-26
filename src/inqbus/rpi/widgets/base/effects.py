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


class Effect(object):
    """
    Base of Effect adapters. Having its own thread enables adapters to be used for asynchronous efects as
    blinking, scrolling, etc of a widget.
    """
    def __init__(self, widget, display):
        self.widget = widget
        self.display = display
        # Signal Queue to control the effects thread
        self.queue = Queue()
        self.init()

    def __call__(self, delay=0.5):
        self.delay = delay
        # Start the thread
        self.thread = threading.Thread(target=self.run, args =(self.queue, ))
        self.thread.start()

    def init(self):
        pass

    def run(self, queue):
        pass

    def done(self):
        """
        Halt the blinking
        :return: None
        """
        self.queue.put(True)



@implementer(IBlinking)
class Blinking(Effect):
    """
    Adapter for blinking widgets. This adapter starts its own thread to render the widget on/off after blink_delay seconds.
    """
    __used_for__ = (IWidget, IDisplay)

    def change_widget(self):
        pass

    def run(self, queue):
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
                sleep(self.delay)
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
            self.change_widget()
            sleep(self.delay)
            renderer.clear()
            sleep(self.delay)



gsm = getGlobalSiteManager()
gsm.registerAdapter(Blinking, (IWidget, IDisplay), IBlinking)


@implementer(IScrolling)
class Scrolling(Blinking):
    """
    Adapter for scrolling widgets
    """
    __used_for__ = (IWidget, IDisplay)

    def init(self):
        """
        Generate a cyclic generator of scroll positions
        :return:
        """
        def _next_pos():
            while True:
                for i in range(self.widget.length):
                    yield i

        self.next_pos = _next_pos()


    def change_widget(self):
        """
        Set the new scroll position by the cycly generator
        :return:
        """
        # set the scroll position on the widget
        self.widget.scroll_pos = self.next_pos.__next__()


gsm = getGlobalSiteManager()
gsm.registerAdapter(Scrolling, (IWidget, IDisplay), IScrolling)
