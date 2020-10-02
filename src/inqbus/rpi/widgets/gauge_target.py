from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.gauge import Gauge
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer

from inqbus.rpi.widgets.interfaces.widgets import (
    IGaugeTargetWidget, )
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(IGaugeTargetWidget)
class GaugeTarget(Gauge):
    """
    Gauge Widget. Representing a single line Gauge.
    """
    _can_focus = True

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
        super(Gauge, self).__init__(label=label, **kwargs)
        self._desired_height = 1
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

    def render_content(self):
        """
        Render the Gauge at the given position

        Returns: the new x, y position
        """

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
            else:
                fc['operator'] = '>'


        out_str = """{label}:{reading:{format}}{operator}{level:{format}}{unit}""".format(**fc)  # noqa: E501

        out_str_focus = self.render_focus(out_str)
        return out_str_focus


# Register the adapters
gsm = getGlobalSiteManager()
gsm.registerAdapter(
        GaugeTargetRenderer,
        (IGaugeTargetWidget, Interface),
        IRenderer)
