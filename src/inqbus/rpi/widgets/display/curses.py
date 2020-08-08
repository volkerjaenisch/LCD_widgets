import curses

from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.interfaces.widgets import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class DisplayCurses(Display):

    def init(self):
        curses.initscr()
        self.display = curses.newwin(self.line_count, self.chars_per_line, 0, 0)
        self.display.clear()

    def write(self, line):
        self.display.addstr(self.pos_y, self.pos_x, line)

