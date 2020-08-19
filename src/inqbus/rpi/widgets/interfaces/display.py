from inqbus.rpi.widgets.interfaces.interfaces import IDevice

class IDisplayHardware(IDevice):
    """
    Interface to hardware display
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
    Abstraction of the hardware. Dealing with out of bounds coordinates and so the like.
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


class IRPLCD(IDisplay):
    pass


class ICharLCD(IDisplay):
    pass


class ICurses(IDisplay):
    pass
