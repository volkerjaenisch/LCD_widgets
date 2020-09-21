from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.input.pynput_input import PynputInput
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from inqbus.rpi.widgets.line import Line
from inqbus.rpi.widgets.page import Page
from inqbus.rpi.widgets.select import Select

from zope.component import getUtility


import inqbus.rpi.widgets.gui  # noqa: W06111
import inqbus.rpi.widgets.base.controller  # noqa: W06111


gui = getUtility(IGUI)

display = Display()
gui.add_display(display)

input = PynputInput()
gui.add_input(input)

gui.init()


layout = Page()

line = Line()
line.content = 'huhu'
layout.add_widget(line)

select = Select(pos_y=1, line_count=4)
select.content = [
    'sel1',
    'sel2',
    'sel3',
    'sel4',
]

layout.add_widget(select)

gui.set_layout(layout)


gui.run()
