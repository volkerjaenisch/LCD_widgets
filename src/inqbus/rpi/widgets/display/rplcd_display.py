from RPLCD.i2c import CharLCD
from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class RPLCDDisplay(Display):

    def __init__(self,
                 height,
                 width,
                 i2c_expander,
                 address,
                 expander_params=None,
                 port=1,
                 dotsize=8,
                 charmap='A02',
                 auto_linebreaks=True,
                 backlight_enabled=True,
                 autoupdate=True):
        self.i2c_expander = i2c_expander
        self.address = address
        self.port = port
        self.expander_params = expander_params
        self.dotsize = dotsize
        self.charmap = charmap
        self.auto_linebreaks = auto_linebreaks
        self.backlight_enabled=backlight_enabled
        super(RPLCDDisplay, self).__init__(height, width, autoupdate=True)

    def init(self, display=None):
        super(RPLCDDisplay, self).init()
        self.display = CharLCD(
                self.i2c_expander,
                self.address,
                port=self.port,
                cols=self.width,
                rows=self.height,
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
