from inqbus.rpi.widgets.display.console import ConsoleDisplay
from inqbus.rpi.widgets.display.rplcd_display import RPLCDDisplay
from inqbus.rpi.widgets.input.rotary_encoder import RotaryInput
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from inqbus.rpi.widgets.widgets import Page, Line, Lines, Select, Button

from zope.component import getUtility

import inqbus.rpi.widgets.gui # IMPORTANT!
import inqbus.rpi.widgets.render # IMPORTANT!
import inqbus.rpi.widgets.widgets # IMPORTANT!
import inqbus.rpi.widgets.controllers # IMPORTANT!
import inqbus.rpi.widgets.base.controller # IMPORTANT!
import inqbus.rpi.widgets.base.notify # IMPORTANT!
import inqbus.rpi.widgets.base.focus # IMPORTANT!

def button_clicked():
    print('Button Clicked!')
    return True

layout = Page()

line = Button()
line.content = 'huhu' + '↑'
line.click_handler = button_clicked

layout.add_widget(line)

text = Lines()
text.content = ["Hallo",
                "Welt"]

select = Select(pos_y=1, height=3)
select.content = [
    'sel1',
    text,
    'sel3',
    'sel4',
    'sel5',
    'sel6',
    'sel7',
]

layout.add_widget(select)

gui = getUtility(IGUI)
display = ConsoleDisplay()
gui.add_display(display)
display = RPLCDDisplay(4, 20, 'PCF8574', 0x27)
gui.add_display(display)

input = RotaryInput()
gui.add_input(input)

gui.set_layout(layout)

gui.focus = line

gui.init()
gui.run()
