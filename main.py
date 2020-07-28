from base.controller import Controller
from base.display import Display
from display.curses import CursesDisplay
#from input.rotary_encoder import InputRotary
from widgets import Page, Line, Select


display = CursesDisplay()
controller = Controller()
controller.register_display(display)

start_page = Page(controller)

header = Line((0, 0))
body = Select((1,0), 3 )

start_page.add_widget(header)
start_page.add_widget(body)

header.content = 'Hallo'
body.content = ['Volker', 'Du', 'Aas']

header.content = 'Huhu'

controller.active_page = start_page

controller.loop_curses(display)
