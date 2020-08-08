from inqbus.rpi.widgets.interfaces.widgets import IWidget, IGUI
from zope.interface import implementer
from zope.component import getGlobalSiteManager
gsm = getGlobalSiteManager()



@implementer(IGUI)
class GUI(object):
    _displays = None
    _inputs = None
    _layout = None

    def setup(self, inputs, displays, layout):
        self._inputs = inputs
        self._displays = displays
        self._layout = layout

    def run(self):
        for display in self._displays:
            display.init()
            display.run()
        self._layout.init()
        for input in self._inputs:
            input.init(self._layout)
            input.run()


gui = GUI()
gsm.registerUtility(gui, IGUI)
