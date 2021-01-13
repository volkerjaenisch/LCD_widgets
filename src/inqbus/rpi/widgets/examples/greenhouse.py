from inqbus.rpi.widgets.checkbox import Checkbox
from inqbus.rpi.widgets.display.rplcd_display import RPLCDDisplay
from inqbus.rpi.widgets.gauge import Gauge
from inqbus.rpi.widgets.gauge_target import GaugeTarget
from inqbus.rpi.widgets.input.rotary_encoder import RotaryInput
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from inqbus.rpi.widgets.page import Page
from zope.component import getUtility

# load the gui component
import inqbus.rpi.widgets.gui  # noqa: W06111
# load the base controller component
import inqbus.rpi.widgets.base.controller  # noqa: W06111


gui = getUtility(IGUI)

display2 = RPLCDDisplay(4, 20, 'PCF8574', 0x27)
gui.add_display(display2)
input = RotaryInput()
gui.add_input(input)

page = Page()

gauge1 = Gauge(
        label='T',
        initial_value=20,
        format='.1f',
        unit='°C',
        increment=5,
        fixed_pos=True,
        read_only=True,
)
page.add_widget(gauge1)

gauge2 = Gauge(
        pos_y=0,
        pos_x=10,
        label='RH',
        initial_value=80,
        format='.1f',
        unit='%',
        read_only=True,
        fixed_pos=True,
)
page.add_widget(gauge2)



sub_page = Page(
        pos_y=1,
        pos_x=0)

page.add_widget(sub_page)


gauge3 = GaugeTarget(
        label='Mois.',
        initial_value=1.6,
        initial_reading_value=1.6,
        increment=0.1,
        fixed_pos=True
)
sub_page.add_widget(gauge3)

irrigation = Checkbox(
        label='Irrigation',
)
sub_page.add_widget(irrigation)

pump = Checkbox(
        label='Pumping',
)
sub_page.add_widget(pump)

otto = Checkbox(
        label='Otto',
)
sub_page.add_widget(otto)


gui.set_layout(page)

page.controller.acquire_focus()


gui.init()
gui.run(blocking=True)

gui.done()
