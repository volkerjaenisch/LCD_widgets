from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.errors import OutOfDisplay
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class ConsoleDisplay(Display):

    def __init__(self,
                 height=4,
                 width=20,
                 autoupdate=True,
                 ):
        super(ConsoleDisplay, self).__init__(
                height=height,
                width=width,
                autoupdate=autoupdate
        )
        self.init()

    def init(self):
        super(ConsoleDisplay, self).init()
        self.display = [ ' ' * self.width for i in range(self.height)]

    def run(self):
        pass

    def done(self):
        pass

    def write(self, content):
        current_line = self.display[self.pos_y]
        current_line = current_line[0:self.pos_x] + content + current_line[self.pos_x + len(content):]
        current_line = current_line[0:self.width]
        self.display[self.pos_y] = current_line
        if self.autoupdate:
            self.show()

    def show(self):
        print('+' + '-' * self.width + '+')
        for line in self.display:
            print('|' + line + '|')
        print('+' + '-' * self.width + '+')

