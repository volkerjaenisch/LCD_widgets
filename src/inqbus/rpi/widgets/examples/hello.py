from time import sleep
from inqbus.rpi.widgets.display.curses import DisplayCurses
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from inqbus.rpi.widgets.text import Text
from zope.component import getUtility

# load the gui component
import inqbus.rpi.widgets.gui  # noqa: W06111
# load the base controller component
import inqbus.rpi.widgets.base.controller  # noqa: W06111

text = Text()
text.content = 'Hello World'

gui = getUtility(IGUI)
display = DisplayCurses()

gui.add_display(display)
gui.set_layout(text)

gui.init()
gui.run(blocking=False)

while True:
    sleep(1)
    text.clear()
    text.pos_y = (text.pos_y + 1) % 4
    text.render()

gui.done()
