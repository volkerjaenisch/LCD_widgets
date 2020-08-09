from RPLCD.i2c import CharLCD
from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.interfaces.widgets import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class DisplayCharLCD(Display):

    def init(self):

        self.display = CharLCD('PCF8574', 0x27, backlight_enabled=True)
#        self.lcd = CharLCD('MCP23017', 0x20, backlight_enabled=True, expander_params={'gpio_bank': 'B'})
        self.display.clear()

    def set_cursor_pos(self, y, x):
        self.display.cursor_pos = (y, x)

    def write(self, line):
        self.display.write_string(line)


