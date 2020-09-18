from time import sleep
from inqbus.rpi.widgets.display.curses import DisplayCurses
from inqbus.rpi.widgets.display.rplcd_display import RPLCDDisplay
from inqbus.rpi.widgets.gauge import Gauge
from inqbus.rpi.widgets.input.rotary_encoder import RotaryInput
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from zope.component import getUtility

# load the gui component
import inqbus.rpi.widgets.gui # IMPORTANT!
# load the base controller component
import inqbus.rpi.widgets.base.controller # IMPORTANT!

gauge = Gauge(label='Temperature', initial_value=20, unit='°', increment=5)

gui = getUtility(IGUI)

display2 = RPLCDDisplay(4, 20, 'PCF8574', 0x27)
gui.add_display(display2)

#display = DisplayCurses()
#gui.add_display(display)

gui.set_layout(gauge)

input = RotaryInput()
gui.add_input(input)

gui.init()
gui.run(blocking=True)

gui.done()
