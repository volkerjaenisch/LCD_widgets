from inqbus.rpi.widgets.base.controller import WidgetController
from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.interfaces.interfaces import (
    IRenderer,
    IWidgetController, )
from inqbus.rpi.widgets.interfaces.widgets import IButtonWidget
from inqbus.rpi.widgets.line import Line
from inqbus.rpi.widgets.base.signals import Input_Click
from zope.component import getGlobalSiteManager
from zope.interface import implementer, Interface


@implementer(IButtonWidget)
class Button(Line):
    """
    Button Widget. Representing a single line button.
    """
    # The click_handler for the button
    _click_handler = None

    @property
    def width(self):
        """
        :return: the width of the widget in characters
        """
        if self._desired_width is None:
            # The button adds two braces so we have to add 2 to width if we calculate it based on the content
            return len(self.content) + 2
        else:
            return self._desired_width

    @width.setter
    def width(self, value):
        """
        Set the width to a fixed value
        :param value: width
        """
        self._desired_width = value

    def init_content(self):
        # The initial content of the button should be empty as long as no content is set
        self._content = ''

    @property
    def click_handler(self):
        """
        Property to get the click_handler
        :return: the click_handler
        """
        return self._click_handler

    @click_handler.setter
    def click_handler(self, handler):
        """
        Property to set the click_handler
        :param handler: The handler
        :return: None
        """
        self._click_handler = handler


@implementer(IRenderer)
class ButtonRenderer(Renderer):
    """
    Renderer for a LineWidget
    """
    __used_for__ = (IButtonWidget, Interface)

    def render(self):
        """
        Render the Button at the given position
        :return: the new x, y position
        """
        pos_x = self.widget.pos_x
        pos_y = self.widget.pos_y
        # if a button width is set truncate the content
        if self.widget.width:
            # when we render the button we have to substract two characters for the braces to determine
            # the amount of characters to frame_buffer.
            content = self.widget.content[:self.widget.width-2]
        else:
            content = self.widget.content

        # If the button is focussed indicate this by changing the braces to angles
        if self.widget.has_focus:
            out_str = '>' + content + '<'
        else:
            out_str = '[' + content + ']'
        self.display.write_at_pos(pos_x, pos_y, out_str)
        # return the coordinate after the content
        # ToDo width, height handling
        return pos_x, pos_y + 1

    def clear(self):
        """
        Erase the button from the frame_buffer
        :return:
        """
        self.display.write_at_pos(self.widget.pos_x, self.widget.pos_y, ' ' * (len(self.widget.content) + 2))


@implementer(IWidgetController)
class ButtonController(WidgetController):
    """
    Controller for IButtonWidgets.
    """
    __used_for__ = (IButtonWidget)

    def notify(self, signal):
        """
        Dispatcher for Signals. Displaytches only the Input_Click signal
        :param signal: Incoming Signal
        :return: True if the widget consumes the Signal, False if the widget cannot consume signal
        """
        if signal == Input_Click:
            return self.widget.click_handler()
        else:
            return False


# Register the adapters
gsm = getGlobalSiteManager()
gsm.registerAdapter(ButtonRenderer, (IButtonWidget, Interface), IRenderer)
gsm.registerAdapter(ButtonController, (IButtonWidget,), IWidgetController)
