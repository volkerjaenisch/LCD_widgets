from inqbus.rpi.widgets.display.curses import DisplayCurses
from inqbus.rpi.widgets.input.curses import InputCurses
from inqbus.rpi.widgets.interfaces.widgets import IGUI
from inqbus.rpi.widgets.widgets import Page, Line

from zope.component import getUtility


import inqbus.rpi.widgets.gui # IMPORTANT!
import inqbus.rpi.widgets.render # IMPORTANT!
import inqbus.rpi.widgets.base.widget_controller # IMPORTANT!
import inqbus.rpi.widgets.base.notify # IMPORTANT!


gui = getUtility(IGUI)


display = DisplayCurses()
input = InputCurses(display)

layout = Page((0,0),4)

line = Line((0,0))
line.content = 'huhu'

layout.add_widget(line)

gui.setup(inputs=[input], displays=[display], layout=layout)

gui.run()

