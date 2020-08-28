from inqbus.rpi.widgets.base.signals import Input_Down, Input_Up, Input_Click

# Mapping of keyboard characters to Input Signals
KEYBOARD_SIGNALS = {
    'u': Input_Up,
    'd': Input_Down,
    'c': Input_Click
}

