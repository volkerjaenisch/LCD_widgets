from inqbus.rpi.widgets.errors import OutOfDisplay
from inqbus.rpi.widgets.interfaces.widgets import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class Display(object):

    def __init__(self,
                 line_count=4,
                 chars_per_line=20,
                 autoupdate=True,
                 ):
        self.autoupdate = autoupdate
        self.line_count = line_count
        self.chars_per_line = chars_per_line
        self.pos_x = 0
        self.pos_y = 0
        self.init()

    def init(self):
        self.display = [ ' ' * self.chars_per_line for i in range(self.line_count)]

    def run(self):
        pass

    def done(self):
        pass

    def write_at_pos(self, x, y, content):
        try:
            self.set_cursor_pos(x, y)
            self.write(content)
        except OutOfDisplay:
            return

    def set_cursor_pos(self, x, y):
        if not y < self.line_count :
            raise OutOfDisplay
        if not x < self.chars_per_line :
            raise OutOfDisplay
        self.pos_x, self.pos_y = (x, y)

    def write(self, content):
        current_line = self.display[self.pos_y]
        current_line = current_line[0:self.pos_x] + content + current_line[self.pos_x + len(content):]
        current_line = current_line[0:self.chars_per_line]
        self.display[self.pos_y] = current_line
        if self.autoupdate:
            self.show()

    def show(self):
        print('+' + '-' * self.chars_per_line + '+')
        for line in self.display:
            print('|' + line + '|')
        print('+' + '-' * self.chars_per_line + '+')

