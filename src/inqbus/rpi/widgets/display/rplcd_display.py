from RPLCD.i2c import CharLCD
from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.interfaces.widgets import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class RPLCDDisplay(Display):

    def __init__(self,
                 line_count,
                 chars_per_line,
                 i2c_expander,
                 address,
                 expander_params=None,
                 port=1,
                 dotsize=8,
                 charmap='A02',
                 auto_linebreaks=True,
                 backlight_enabled=True):
        self.chars_per_line = chars_per_line
        self.line_count = line_count
        self.i2c_expander = i2c_expander
        self.address = address
        self.port = port
        self.expander_params = expander_params
        self.dotsize = dotsize
        self.charmap = charmap
        self.auto_linebreaks = auto_linebreaks
        self.backlight_enabled=backlight_enabled

    def init(self, display=None):
        self.display = CharLCD(
                self.i2c_expander,
                self.address,
                port=self.port,
                cols=self.chars_per_line,
                rows=self.line_count,
                expander_params=self.expander_params,
                dotsize=self.dotsize,
                charmap=self.charmap,
                auto_linebreaks=self.auto_linebreaks,
                backlight_enabled=self.backlight_enabled,
        )
        self.display.clear()

    def set_cursor_pos(self, x, y):
        super(RPLCDDisplay, self).set_cursor_pos(x,y)
        self.display.cursor_pos = (y, x)

    def write(self, line):
        self.display.write_string(line)

    def show(self):
        pass
