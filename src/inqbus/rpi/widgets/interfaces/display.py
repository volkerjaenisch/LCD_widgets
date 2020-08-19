from inqbus.rpi.widgets.interfaces.interfaces import IDevice


class IDisplayHardware(IDevice):
    """
    Interface to display driver
    """

    def set_cursor_pos(self, x, y):
        """
        Set the cursor at position
        :param x:
        :param y:
        :return:
        """

    def write(self, line):
        """
        Write a string at the cursor position
        :param line:
        :return:
        """


class IDisplay(IDisplayHardware):
    """
    Abstraction of the display driver. Dealing with out of bounds coordinates and so the like.
    """

    def write_at_pos(self, x, y, content):
        """
        Write a string at a given display position
        :param x:
        :param y:
        :param content:
        :return:
        """
    def set_cursor_pos(self, x, y):
        """
        Set the sursor to a certain position
        :param x:
        :param y:
        :return:
        """


class IConsoleDisplay(IDisplay):
    """
    Display of the char display in the console of the host
    """


class IRPLCD(IDisplay):
    """
    Integration of RPLCD  https://pypi.org/project/RPLCD/
    driven Character displays.
    """


class ICharLCD(IDisplay):
    """
    Integration of CharLCD  https://pypi.org/project/charlcd/
    driven Character displays.
    """


class ICurses(IDisplay):
    """
    Curses integration
    """
