from inqbus.rpi.widgets.base.controller import WidgetController
from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.base.signals import InputClick, InputUp, InputDown
from inqbus.rpi.widgets.interfaces.interfaces import (
    IRenderer, IWidgetController
)
from inqbus.rpi.widgets.interfaces.widgets import IGaugeWidget
from inqbus.rpi.widgets.line import Line
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(IGaugeWidget)
class Gauge(Line):
    """
    Gauge Widget. Representing a single line Gauge.
    """

    # Value callback
    _value_callback = None
    _up_handler = None
    _down_handler = None

    def __init__(
            self,
            label,
            initial_value=0,
            increment=1,
            unit=None,
            format='.2f',
            read_only=False,
            value_callback=None,
            up_handler=None,
            down_handler=None,
            **kwargs,
    ):
        super(Gauge, self).__init__(label=label, **kwargs)
        self._desired_height = 1
        self._content = initial_value
        self._increment = increment
        self._format = format
        self._unit = unit
        self._value_callback = value_callback
        self._up_handler = up_handler
        self._down_handler = down_handler
        self.is_activated = False
        self.is_read_only = read_only

    @property
    def width(self):
        """
        The width of the widget in characters
        """
        if self._desired_width is None:
            # The Gauge adds two braces
            # so we have to add 2 to the width of the content itself
            return len(self.content) + 2
        else:
            return self._desired_width

    @width.setter
    def width(self, value):
        """
        Set the width to a fixed value

        Args:
            value: width
        """
        self._desired_width = value

    def init_content(self):
        # The initial content of the Gauge should
        # be empty as long as no content is set
        if self._value_callback is not None:
            self._content = self._value_callback(self._content)
        else:
            self._content = ''

    def click_handler(self):
        """
        If clicked the toggle activated/deactivated

        Returns:
            True
        """
        if self.is_read_only:
            return False
        self.is_activated = not self.is_activated
        if self.render_on_content_change:
            self.render()
        return True

    def up_handler(self):
        """
        Handles up signal

        Returns:
            False: If the widget is not activated
            True: Else
        """
        if not self.is_activated:
            return False
        if self._up_handler is not None:
            self._up_handler(self, self._content)
        else:
            self._content += self._increment
        if self.render_on_content_change:
            self.render()
        return True

    def down_handler(self):
        """
        Handles down signal

        Returns:
            False: If the widget is not activated
            True: Else
        """
        if not self.is_activated:
            return False
        if self._down_handler is not None:
            self._down_handler(self, self._content)
        else:
            self._content -= self._increment
        if self.render_on_content_change:
            self.render()
        return True

    def release_focus(self):
        self.is_activated = False
        super(Gauge, self).release_focus()


@implementer(IRenderer)
class GaugeRenderer(Renderer):
    """
    Renderer for a LineWidget
    """
    __used_for__ = (IGaugeWidget, Interface)

    def render_content(self):
        fc = {}
        # Label handling
        if self.widget._label is not None:
            fc['label'] = self.widget._label
        else:
            fc['label'] = ''

        # If the Gauge is activated
        if self.widget.is_activated:
            fc['operator'] = '?'
        else:
            if fc['label']:
                fc['operator'] = ':'
            else:
                fc['operator'] = ''

        # Do we have a unit?
        if self.widget._unit is not None:
            fc['unit'] = self.widget._unit
        else:
            fc['unit'] = ''

        # Handling of the content
        fc['content'] = self.widget.content
        fc['format'] = self.widget._format

        out_str = '{label}{operator}{content:{format}}{unit}'.format(**fc)

        return self.render_focus(out_str)


@implementer(IWidgetController)
class GaugeController(WidgetController):
    """
    Controller for IButtonWidgets.
    """
    __used_for__ = IGaugeWidget

    def dispatch(self, signal):
        """
        Dispatcher for Signals. Displaytches only the InputClick signal

        Args:
            signal: Incoming Signal

        Returns:
            True if the widget consumes the Signal,
            False if the widget cannot consume the signal
        """
        result = False
        if signal == InputClick:
            result = self.widget.click_handler()
        elif signal == InputUp:
            result = self.widget.up_handler()
        elif signal == InputDown:
            result = self.widget.down_handler()

        if not result:
            return self.widget.parent.controller.dispatch(signal)


# Register the adapters
gsm = getGlobalSiteManager()
gsm.registerAdapter(GaugeRenderer, (IGaugeWidget, Interface), IRenderer)
gsm.registerAdapter(GaugeController, (IGaugeWidget,), IWidgetController)
