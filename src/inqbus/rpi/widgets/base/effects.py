"""
Adapters for visual effects on widgets. E.G. blinking, scrolling
"""

import threading
from abc import ABC
from queue import Queue, Empty
from wrapt import ObjectProxy
from time import sleep

from inqbus.rpi.widgets.interfaces.display import IDisplay
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.effects import (
    IBlinking, IScrolling,
    IScrollWrapper, )
from inqbus.rpi.widgets.interfaces.widgets import IWidget
from zope.component import getGlobalSiteManager, getMultiAdapter
from zope.interface import implementer, alsoProvides


class Effect(object):
    """
    Base of Effect adapters. Having its own thread enables
    adapters to be used for asynchronous efects as
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
        self.thread = threading.Thread(target=self.run, args=(self.queue, ))
        self.thread.start()

    def init(self):
        """
        Initialize the effect
        """
        pass

    def get_renderer(self):
        renderer = getMultiAdapter(
                (self.widget, self.display),
                interface=IRenderer
        )
        return renderer

    def render(self):
        """
        Render the effect
        """
        self.renderer.render()

    def clear(self):
        """
        Clear the effect
        """
        self.renderer.clear()

    def run(self, queue):
        """
        Run the effect on the widget.
        If the calling thread put anything into the queue the effect will stop.

        Args:
            queue: The given Queue connects the Effect with its callers thread.

        Returns:
            None
        """

        # get the renderer for the widget/frame_buffer
        self.renderer = self.get_renderer()
        while True:
            # Not initilized yet?
            if not self.display.initialized:
                sleep(self.delay)
                continue
            # Render the widget. This is important to prevent
            # an empty widget when blinking stops
            self.render()
            # check for stopping the blinking
            try:
                # get a signal from the queue
                _ = queue.get(block=False)
                # if we got a signal break the loop/end the thread
                break
            # if the queue is empty we have to continue
            except Empty:
                pass
            sleep(self.delay)
            self.clear()
            sleep(self.delay)

    def done(self):
        """
        Finishes the effect. E.g. stop it.

        Returns:
            None
        """
        self.queue.put(True)


@implementer(IBlinking)
class Blinking(Effect):
    """
    Adapter for blinking widgets.
    """
    __used_for__ = (IWidget, IDisplay)


@implementer(IScrollWrapper)
class ScrollWrapper(ObjectProxy, ABC):
    """
    Wrapper around a Widget to modify its content state.
    """
    __used_for__ = IWidget

    def __init__(self, wrapped):
        super(ScrollWrapper, self).__init__(wrapped)
        # Add to the wrapper instance the same interfaces
        # that the wrapped instance has
        alsoProvides(self, self.__wrapped__.__provides__)

    def __call__(self, effect):
        # Store a reference to the effect instance
        self.effect = effect

    @property
    def content(self):
        # get the origina content ..
        cont = self.__wrapped__.content
        # .. and the curretn scroll position
        scroll_pos = self.effect.scroll_pos
        # and return only the portion of the content after the scroll_pos
        return cont[scroll_pos:]


@implementer(IScrolling)
class Scrolling(Blinking):
    """
    Adapter for scrolling widgets
    """
    __used_for__ = (IWidget, IDisplay)

    def init(self):
        # initialize the scrolling position to the first character
        self.scroll_pos = 0
        # get a reference for the scroll_pos generator
        self.next_pos = self._next_pos()

    def _next_pos(self):
        """
        Generator for scroll positions. Generates circular char positions.

        Returns:
            None
        """
        # circular
        while True:
            # for each position in the content
            for i in range(self.widget.length):
                # yield the position
                yield i

    def get_renderer(self):
        """
        Returns the wrapper in place of the widget itself

        Returns:
        """
        # Get the wrapper
        scrolling_widget = IScrollWrapper(self.widget)
        # Get the wrappe a reference of the scrollingController
        # to get access to the generator.
        scrolling_widget(self)
        # retrieve the renderer for the wrapper and the current frame_buffer.
        renderer = getMultiAdapter(
                (scrolling_widget, self.display),
                interface=IRenderer
        )
        # Return the renderer
        return renderer

    def render(self):
        # get the next scroll_position from the generator
        self.scroll_pos = self.next_pos.__next__()
        # do the rendering. While rendering the renderer will
        # request the content of the wrapper. The wrapper will
        # use the self.scroll_pos to deliver only the
        # appropriate string portion.
        super(Scrolling, self).render()


gsm = getGlobalSiteManager()
gsm.registerAdapter(Blinking, (IWidget, IDisplay), IBlinking)
gsm.registerAdapter(Scrolling, (IWidget, IDisplay), IScrolling)
gsm.registerAdapter(ScrollWrapper, (IWidget,), IScrollWrapper)
