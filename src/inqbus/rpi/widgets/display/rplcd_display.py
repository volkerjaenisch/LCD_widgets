from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.interfaces.display import IDisplay
from RPLCD.i2c import CharLCD
from zope.interface import implementer


@implementer(IDisplay)
class RPLCDDisplay(Display):
    """
    Display class for character displays via the RPLCD python driver
    https://rplcd.readthedocs.io/en/stable/
    Please find the explanation of the parameters there.
    """

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
        self.backlight_enabled = backlight_enabled
        self.autoupdate = autoupdate
        super(RPLCDDisplay, self).__init__(height, width, autoupdate=True)

    def init(self, display=None):
        """
        Bring up the frame_buffer.
        :param display:
        :return:
        """
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
        # Clear the frame_buffer
        self.display.clear()
        self.initialized = True

    def set_cursor_pos(self, x, y):
        """
        Set the position of the cursor.
        This function should not be called directly,
        since it is not thread safe
        Call the write_at(x,y,value) instead,
        which subsequently calls set_cursor_pos for you
        and is thread safe.
        :param x: X position in characters
        :param y: Y position in characters
        :return:
        """
        if not self.initialized:
            return
        super(RPLCDDisplay, self).set_cursor_pos(x, y)
        self.display.cursor_pos = (y, x)

    def write(self, value):
        """
        Write a string to the frame_buffer.
        This function should not be called directly,
        since it is not thread safe.
        Call the write_at(x,y,value) instead,
        which subsequently calls set_cursor_pos for you
        and is thread safe.
        :param value: The string to be written
        :return:
        """
        if not self.initialized:
            return
        self.display.write_string(value)

    def show(self):
        """
        Not used since the frame_buffer reacts immedialtely.
        :return:
        """
        pass
