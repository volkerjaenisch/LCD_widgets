import unittest

from inqbus.rpi.widgets.display.console import ConsoleDisplay
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from zope.component import getUtility


class TestBase(unittest.TestCase):

    def setUp(self):
        self.display = ConsoleDisplay()
        self.gui = getUtility(IGUI)
        self.gui.add_display(self.display)


    def widget_test(self, widget):
        self.gui.set_layout(widget)
        self.gui.render()

