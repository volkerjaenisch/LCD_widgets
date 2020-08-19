import threading
from queue import Queue, Empty
from time import sleep

from inqbus.rpi.widgets.interfaces.widgets import (
    IWidget, )
from inqbus.rpi.widgets.interfaces.interfaces import (
    IWidgetController,
    INotify, IMoveFocus, IGUI, )
from inqbus.rpi.widgets.interfaces.input import IBlockingInput
from zope.interface import implementer, provider
from zope.component import getGlobalSiteManager

gsm = getGlobalSiteManager()


@implementer(IGUI, IWidgetController)
class GUI(object):


    def __init__(self):
        self._displays = []
        self._inputs = []
        self._layout = None
        self._focus = None
        self.signal_queue = Queue()

    def add_display(self, display):
        self._displays.append( display )

    def add_input(self, input):
        self._inputs.append(input)

    def set_layout(self, layout):
        self._layout = layout
        self._focus= self._layout

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, widget):
        self._focus = widget

    def init(self):
        for display in self._displays:
            display.init()
            display.run()
        for input in self._inputs:
            input.init()
            if IBlockingInput.providedBy(input):
                thread = threading.Thread(target=input.run, args =(self.signal_queue, ))
                thread.start()
            else:
                input.run()

    def run(self):
        self._layout.render()
        self.signal_loop()

    def signal_loop(self):
        while True:
            sleep(0.1)
            try:
                signal = self.signal_queue.get(block=False)
                self.notify(signal)
            except Empty:
                pass

    def notify(self, signal):
        notify = INotify(self.focus.controller)
        result = notify.notify(signal)
        if result:
            return result
        else:
            IMoveFocus(self)(signal)
            return True


    @property
    def displays(self):
        return self._displays

    def render(self):
        self._layout.render()


gui = GUI()
gsm.registerUtility(gui, IGUI)
