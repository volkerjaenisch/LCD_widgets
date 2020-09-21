from inqbus.rpi.widgets.base.signals import InputDown, InputUp, InputClick

# Mapping of keyboard characters to Input Signals
KEYBOARD_SIGNALS = {
    'u': InputUp,
    'd': InputDown,
    'c': InputClick
}
