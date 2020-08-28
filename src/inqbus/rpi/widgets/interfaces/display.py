from inqbus.rpi.widgets.interfaces.interfaces import IDevice


class IDisplayHardware(IDevice):
    """
    Interface to frame_buffer driver
    """

    def set_cursor_pos(self, x, y):
        """
        Set the cursor at position. This function should not be called directly but only from
        write_at_pos to keep access to the frame_buffer atomic.
        :param x:
        :param y:
        :return:
        """

    def write(self, line):
        """
        Write a string at the cursor position. This function should not be called directly but only from
        write_at_pos to keep access to the frame_buffer atomic.
        :param line:
        :return:
        """


class IDisplay(IDisplayHardware):
    """
    Abstraction of the frame_buffer driver. Dealing with out of bounds coordinates and so the like.
    """

    def write_at_pos(self, x, y, content):
        """
        Write a string at a given frame_buffer position. This atomic operation has to be secured by a threadsafe Lock.
        It calls "set_cursor_pos" and then "write" of the device.
        :param x:
        :param y:
        :param content:
        :return:
        """


class IConsoleDisplay(IDisplay):
    """
    Display of the char frame_buffer in the console of the host
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
