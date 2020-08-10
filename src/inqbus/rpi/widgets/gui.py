from inqbus.rpi.widgets.interfaces.widgets import IWidget, IGUI
from zope.interface import implementer
from zope.component import getGlobalSiteManager
gsm = getGlobalSiteManager()



@implementer(IGUI)
class GUI(object):

    def __init__(self):
        self._displays = []
        self._inputs = []
        self._layout = None

    def add_display(self, display):
        self._displays.append( display )

    def add_input(self, input):
        self._inputs.append(input)

    def set_layout(self, layout):
        self._layout = layout

    def run(self):
        for display in self._displays:
            display.init()
            display.run()
        for input in self._inputs:
            input.init()
            input.run()
        self._layout.render()

    @property
    def displays(self):
        return self._displays

    def render(self):
        self._layout.render()


gui = GUI()
gsm.registerUtility(gui, IGUI)
