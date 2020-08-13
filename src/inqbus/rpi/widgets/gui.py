import threading
from queue import Queue, Empty
from time import sleep

from inqbus.rpi.widgets.interfaces.widgets import IGUI, INotify
from zope.interface import implementer
from zope.component import getGlobalSiteManager


gsm = getGlobalSiteManager()



@implementer(IGUI)
class GUI(object):

    def __init__(self):
        self._displays = []
        self._inputs = []
        self._layout = None
        self.signal_queue = Queue()

    def add_display(self, display):
        self._displays.append( display )

    def add_input(self, input):
        self._inputs.append(input)

    def set_layout(self, layout):
        self._layout = layout

    def init(self):
        for display in self._displays:
            display.init()
            display.run()
        for input in self._inputs:
            input.init()
            thread = threading.Thread(target=input.run, args =(self.signal_queue, ))
            thread.start()

    def run(self):
        self._layout.render()
        self.signal_loop()

    def signal_loop(self):
        while True:
            sleep(0.1)
            try:
                signal = self.signal_queue.get(block=False)
                notify = INotify(self._layout.controller)
                notify.notify(signal)
            except Empty:
                pass



    @property
    def displays(self):
        return self._displays

    def render(self):
        self._layout.render()


gui = GUI()
gsm.registerUtility(gui, IGUI)
