import curses

from inqbus.rpi.widgets.base.display import Display


class CursesDisplay(Display):

    def init_display(self):
        curses.initscr()
        self.display = curses.newwin(self.line_count, self.chars_per_line, 0, 0)
        self.display.clear()

    def write(self, line):
        self.display.addstr(self.pos_y, self.pos_x, line)

