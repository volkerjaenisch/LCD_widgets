import curses

from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.interfaces.widgets import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class DisplayCurses(Display):

    def init(self):
        curses.initscr()
        self.display = curses.newwin(self.height + 1, self.width, 0, 0)

    def write(self, line):
        if not self.pos_y < self.height :
            return
        if not self.pos_x < self.width :
            return
        self.display.addstr(self.pos_y, self.pos_x, line)
        self.display.refresh()

