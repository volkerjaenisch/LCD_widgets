from time import sleep
from inqbus.rpi.widgets.display.curses import DisplayCurses
from inqbus.rpi.widgets.display.rplcd_display import RPLCDDisplay
from inqbus.rpi.widgets.gauge import Gauge
from inqbus.rpi.widgets.input.rotary_encoder import RotaryInput
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from inqbus.rpi.widgets.page import Page
from zope.component import getUtility

# load the gui component
import inqbus.rpi.widgets.gui # IMPORTANT!
# load the base controller component
import inqbus.rpi.widgets.base.controller # IMPORTANT!


gui = getUtility(IGUI)

display2 = RPLCDDisplay(4, 20, 'PCF8574', 0x27)
gui.add_display(display2)

#display = DisplayCurses()
#gui.add_display(display)

page = Page()

gauge1 = Gauge(label='Temperature', initial_value=20, unit='°', increment=5)
gauge2 = Gauge(label='Humidity', initial_value=80, unit='%', increment=5)

page.add_widget(gauge1)
page.add_widget(gauge2)

gui.set_layout(page)

page.aquire_focus()

input = RotaryInput()
gui.add_input(input)

gui.init()
gui.run(blocking=True)

gui.done()
