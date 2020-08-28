from inqbus.rpi.widgets.base.signal import Signal


class Input_Move(Signal):
    pass


class Input_Click(Signal):
    pass


class Input_Up(Input_Move):
    pass


class Input_Down(Input_Move):
    pass


class Input_Char(Signal):
    """
    The char signal contains the character typed
    """

    def __init__(self, content):
        self.content = content
