from inqbus.rpi.widgets.base.controller import WidgetController
from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.base.signals import InputClick, InputUp, InputDown
from inqbus.rpi.widgets.gauge import Gauge
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer, IWidgetController

from inqbus.rpi.widgets.interfaces.widgets import (
    IGaugeWidget,
    IGaugeTargetWidget, )
from inqbus.rpi.widgets.line import Line
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(IGaugeTargetWidget)
class GaugeTarget(Gauge):
    """
    Gauge Widget. Representing a single line Gauge.
    """

    def __init__(
            self,
            label,
            initial_value=0,
            initial_reading_value=0,
            increment=1,
            format='.2f',
            unit=None,
            read_only=False,
            value_callback=None,
            up_handler=None,
            down_handler=None,
            **kwargs,
        ):
        super(Gauge, self).__init__(**kwargs)
        self._desired_height = 1
        self._label = label
        self._content = initial_value
        self._reading_value = initial_reading_value
        self._increment = increment
        self._format = format
        self._unit = unit
        self._value_callback = value_callback
        self._up_handler = up_handler
        self._down_handler = down_handler
        self.is_activated = False
        self.is_read_only = read_only

    def release_focus(self):
        self.is_activated = False
        super(Gauge, self).release_focus()


@implementer(IRenderer)
class GaugeTargetRenderer(Renderer):
    """
    Renderer for a LineWidget
    """
    __used_for__ = (IGaugeTargetWidget, Interface)

    def render(self):
        """
        Render the Gauge at the given position

        Returns: the new x, y position
        """
        pos_x = self.widget.pos_x
        pos_y = self.widget.pos_y
        # # if a Gauge width is set truncate the content
        # if self.widget.width:
        #     # when we render the Gauge
        #     # we have to substract two characters for the braces to determine
        #     # the amount of characters to use from the content.
        #     content = 'self.widget._content
        # else:
        #     content = self.widget.content

        fc = {}
        # Label handling
        if self.widget._label is not None:
            fc['label'] = self.widget._label
        else:
            fc['label'] = ''


        # Do we have a unit?
        if self.widget._unit is not None:
            fc['unit'] = self.widget._unit
        else:
            fc['unit'] = ''

        # Handling of the content
        fc['reading'] = self.widget._reading_value
        fc['level'] = self.widget._content
        fc['format'] = self.widget._format

        # If the Gauge is activated
        if self.widget.is_activated:
            fc['operator'] = '?'
        else:
            if self.widget._reading_value < self.widget._content:
                fc['operator'] = '<'
            elif self.widget._reading_value == self.widget._content:
                fc['operator'] = '='
            else :
                fc['operator'] = '>'

        # If the Gauge is focussed
        # indicate this by changing the braces to angles
        if self.widget.has_focus:
            fc['focus'] = '>'
        else:
            fc['focus'] = ' '

        out_str = '{focus}{label}:{reading:{format}}{operator}{level:{format}}{unit}'.format(**fc)
        self.display.write_at_pos(pos_x, pos_y, out_str)
        # return the coordinate after the content
        # ToDo width, height handling
        return pos_x, pos_y + 1

    def clear(self):
        """
        Erase the Gauge from the frame_buffer
        """
        self.display.write_at_pos(
                self.widget.pos_x,
                self.widget.pos_y,
                ' ' * (len(self.widget.content) + 2)
        )




# Register the adapters
gsm = getGlobalSiteManager()
gsm.registerAdapter(GaugeTargetRenderer, (IGaugeTargetWidget, Interface), IRenderer)
