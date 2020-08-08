from .base.events import Event


class Input_Move(Event):
    pass


class Input_Click(Event):
    pass


class Input_Up(Input_Move):
    pass


class Input_Down(Input_Move):
    pass

