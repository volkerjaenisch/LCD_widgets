import curses

from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class DisplayCurses(Display):
    """
    Curses frame_buffer.
    """

    def init(self):
        super(DisplayCurses, self).init()
        # Initialize a curses screen
        curses.initscr()
        # hide the cursor
        curses.curs_set(0)
        # get a new window from curses at 0,0 on the active console
        self.display = curses.newwin(self.height + 3, self.width + 2, 0, 0)
        self.initialized = True
        # Draw a frame around the active char display area
        self.draw_frame()

    def draw_frame(self):
        """
        Draw a frame around the active char display area
        """
        self.display.addstr(0, 0, '+' + '-' * self.width + '+')
        for pos_y in range(self.height):
            self.display.addstr(pos_y + 1, 0, '|')
            self.display.addstr(pos_y + 1, self.width + 1, '|')
        self.display.addstr(self.height + 1, 0, '+' + '-' * self.width + '+')

    def write(self, line):
        # chack for range violations
        if not self.initialized:
            return
        if not self.pos_y < self.height:
            return
        if not self.pos_x < self.width:
            return
        # display the given string. Offset the write position into the frame
        self.display.addstr(self.pos_y + 1, self.pos_x + 1, line)
        # rerender
        self.display.refresh()
