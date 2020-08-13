import curses

from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.interfaces.widgets import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class DisplayCurses(Display):

    def init(self):
        curses.initscr()
        self.display = curses.newwin(self.line_count+1, self.chars_per_line, 0, 0)

    def write(self, line):
        if not self.pos_y < self.line_count :
            return
        if not self.pos_x < self.chars_per_line :
            return
        self.display.addstr(self.pos_y, self.pos_x, line)
        self.display.refresh()

