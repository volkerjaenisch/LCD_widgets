from RPLCD.i2c import CharLCD


class DisplayCharLCD(object):

    def __init__(self, line_count=4, chars_per_line=20):
        self.line_count = line_count
        self.chars_per_line = chars_per_line

    def init(self):

        self.display = CharLCD('PCF8574', 0x27, backlight_enabled=True)
#        self.lcd = CharLCD('MCP23017', 0x20, backlight_enabled=True, expander_params={'gpio_bank': 'B'})
        self.display.clear()

    def set_cursor_pos(self, y, x):
        self.display.cursor_pos = (y, x)

    def write(self, line):
        self.display.write_string(line)


