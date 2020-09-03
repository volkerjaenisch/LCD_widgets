from inqbus.rpi.widgets.base.signal import Signal


class InputMove(Signal):
    """
    Signal to move the focus
    """
    pass


class InputClick(Signal):
    """
    Signal to handle a click
    """
    pass


class InputUp(InputMove):
    """
    Signal to move the focus up
    """
    pass


class InputDown(InputMove):
    """
    Signal to move the focus down
    """
    pass


class InputChar(Signal):
    """
    The char signal contains the character typed
    """

    def __init__(self, content):
        self.content = content
