from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.errors import OutOfDisplay
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class ConsoleDisplay(Display):
    """
    Display the changes of the gui on the console. Mostly usefull for debugging or developing on
    a desktop where the real hardware is not available.
    """

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
        """
        INitialize the display. In this case we only build a character "frame buffer"
        :return:
        """
        super(ConsoleDisplay, self).init()
        self.display = [ ' ' * self.width for i in range(self.height)]

    def run(self):
        pass

    def done(self):
        pass

    def write(self, content):
        """
        Write given content to the display at the current cursor position.
        :param content: the content given. String
        :return:
        """
        # copy the line where the cursor is set into new_line
        new_line = self.display[self.pos_y]
        # insert the content into the new_line
        new_line = new_line[0:self.pos_x] + content + new_line[self.pos_x + len(content):]
        # clip new_line with the width of the display
        new_line = new_line[0:self.width]
        # replace the line in the display with the new_line
        self.display[self.pos_y] = new_line
        # if the diplay autoupdate is set ..
        if self.autoupdate:
            # .. show the display
            self.show()

    def show(self):
        """
        Do a simple representation of the display by printing all its lines to the console.
        :return:
        """
        print('+' + '-' * self.width + '+')
        for line in self.display:
            print('|' + line + '|')
        print('+' + '-' * self.width + '+')

