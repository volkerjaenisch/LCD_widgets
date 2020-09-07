import curses

from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class DisplayCurses(Display):
    """
    Curses frame_buffer. CURRENTLY NOT WORKING!
    """

    def init(self):
        super(DisplayCurses, self).init()
        curses.initscr()
        self.display = curses.newwin(self.height + 3, self.width + 2, 0, 0)
        self.write_frame()

    def write_frame(self):
        self.display.addstr(0, 0, '+' + '-' * self.width + '+')
        for pos_y in range(self.height):
            self.display.addstr(pos_y + 1, 0, '|')
            self.display.addstr(pos_y + 1, self.width + 1, '|')
        self.display.addstr(self.height + 1, 0, '+' + '-' * self.width + '+')

    def write(self, line):
        if not self.pos_y < self.height:
            return
        if not self.pos_x < self.width:
            return
        self.display.addstr(self.pos_y + 1, self.pos_x + 1, line)
        self.display.refresh()
