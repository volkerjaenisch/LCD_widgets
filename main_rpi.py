from threading import Timer

from inqbus.rpi.widgets.display.console import ConsoleDisplay
from inqbus.rpi.widgets.display.rplcd_display import RPLCDDisplay
from inqbus.rpi.widgets.input.rotary_encoder import RotaryInput
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from inqbus.rpi.widgets.interfaces.visibility import IBlinking, IScrolling
from inqbus.rpi.widgets.widgets import Page, Line, Lines, Select, Button

from zope.component import getUtility, getMultiAdapter

import inqbus.rpi.widgets.gui # IMPORTANT!
import inqbus.rpi.widgets.render # IMPORTANT!
import inqbus.rpi.widgets.widgets # IMPORTANT!
import inqbus.rpi.widgets.controllers # IMPORTANT!
import inqbus.rpi.widgets.base.controller # IMPORTANT!
import inqbus.rpi.widgets.base.notify # IMPORTANT!
import inqbus.rpi.widgets.base.focus # IMPORTANT!
import inqbus.rpi.widgets.base.visibility # IMPORTANT!

def button_clicked():
    print('Button Clicked!')
    return True

layout = Page()

button1 = Button()
button1.content = 'Marc'
button1.click_handler = button_clicked
layout.add_widget(button1)

button2 = Button()
button2.content = 'otto'
button2.click_handler = button_clicked
layout.add_widget(button2)

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
display1 = ConsoleDisplay()
gui.add_display(display1)
display2 = RPLCDDisplay(4, 20, 'PCF8574', 0x27)
gui.add_display(display2)

input = RotaryInput()
gui.add_input(input)

gui.set_layout(layout)

gui.focus = button1

blink_button  = getMultiAdapter((button1, display2), interface=IBlinking)
fake  = getMultiAdapter((select, display2), interface=IBlinking)()
blink_button()

t = Timer(5, blink_button.done)
t.start()

scroll_button  = getMultiAdapter((button2, display2), interface=IScrolling)
scroll_button()

gui.init()
gui.run()

