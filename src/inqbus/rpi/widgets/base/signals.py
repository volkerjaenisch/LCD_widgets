from inqbus.rpi.widgets.base.signal import Signal


class InputMove(Signal):
    pass


class InputClick(Signal):
    pass


class InputUp(InputMove):
    pass


class InputDown(InputMove):
    pass


class InputChar(Signal):
    """
    The char signal contains the character typed
    """

    def __init__(self, content):
        self.content = content
