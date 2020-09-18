from inqbus.rpi.widgets.base.controller import WidgetController
from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.base.signals import InputClick, InputUp, InputDown
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer, IWidgetController
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

    def __init__(self, label, initial_value=0, increment=1, unit=None, value_callback=None, up_handler=None, down_handler=None):
        super(Line, self).__init__()
        self._desired_height = 1
        self._label = label
        self._content = initial_value
        self._increment = increment
        self._unit = unit
        self._value_callback = value_callback
        self._up_handler = up_handler
        self._down_handler = down_handler
        self.is_activated = False

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

        # Label handling
        if self.widget._label is not None:
            label = self.widget._label
        else:
            label = ''

        # If the Gauge is activated
        if self.widget.is_activated:
            operator = '?'
        else:
            if label:
                operator = ':'
            else:
                operator = ''

        # Do we have a unit?
        if self.widget._unit is not None:
            unit = self.widget._unit
        else:
            unit = ''

        # Handling of the content
        content = str(self.widget.content)

        # If the Gauge is focussed
        # indicate this by changing the braces to angles
        if self.widget.has_focus:
            out_str = '>' + label + operator + content + unit
        else:
            out_str = ' ' + label + ':' + content + unit
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
