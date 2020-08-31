import unittest

from inqbus.rpi.widgets.display.console import ConsoleDisplay
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from zope.component import getUtility

# Important imports to get the framework modules in place
import inqbus.rpi.widgets.base.controller
import inqbus.rpi.widgets.gui


TINY_LINE = 'A'
SHORT_LINE = 'This is a short line'
SHORT_BUTTON = 'Click!'
LONG_LINE = 'This line is really long and will never fit in a display if one consider the typical width of character displays'


class TestBase(unittest.TestCase):

    def setUp(self):
        self.display = ConsoleDisplay()
        self.gui = getUtility(IGUI)
        self.gui.add_display(self.display)

    def tearDown(self):
        self.display.clear()

    def widget_test(self, widget):
        self.display.clear()
        self.gui.set_layout(widget)
        self.gui.render()

