from inqbus.rpi.widgets.base.controller import WidgetController
from inqbus.rpi.widgets.base.signals import InputClick
from inqbus.rpi.widgets.button import Button, ButtonRenderer
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer, IWidgetController

from inqbus.rpi.widgets.interfaces.widgets import (
    IButtonWidget,
    ICheckboxWidget, )
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(ICheckboxWidget)
class Checkbox(Button):
    """
    Button Widget. Representing a single line button.
    """

    # The click_handler for the toggle
    _click_handler = None
    _state = False

    def __init__(self, *args, state=False, **kwargs):
        super(Checkbox, self).__init__(*args, **kwargs)
        self._content = state

    @property
    def content(self):
        if self._state:
            result = 'On'
        else:
            result = 'Off'
        return result

@implementer(IRenderer)
class CheckboxRenderer(ButtonRenderer):
    """
    Renderer for a LineWidget
    """
    __used_for__ = (ICheckboxWidget, Interface)

    def render_focus(self, content):
        # If the checkbox is focussed
        # indicate this by changing the braces to angles
        if self.widget.has_focus:
            out_str = self.special_chars['FOCUS_LEFT'] + self.widget._label + \
                      ':>' + self.widget.content + '<'

        else:
            out_str = ' ' + self.widget._label + ':[' + self.widget.content + ']'
        return out_str

    def render_content(self):
        """
        Render the Checkbox
        """
        # if a button width is set truncate the content
        if self.widget.width:
            # when we render the button
            # we have to substract two characters for the braces to determine
            # the amount of characters to use from the content.
            content = self.widget.content[:self.widget.width-2]
        else:
            content = self.widget.content

        out_str = self.render_focus(content)
        return out_str

@implementer(IWidgetController)
class CheckboxController(WidgetController):
    """
    Controller for IButtonWidgets.
    """
    __used_for__ = ICheckboxWidget

    def dispatch(self, signal):
        """
        Dispatcher for Signals. Displaytches only the InputClick signal

        Args:
            signal: Incoming Signal

        Returns:
            True if the widget consumes the Signal,
            False if the widget cannot consume the signal
        """
        if signal == InputClick:
            self.widget._state = not self.widget._state
            self.widget.render()
            if self.widget.click_handler:
                return self.widget.click_handler()
            return True

        return self.widget.parent.controller.dispatch(signal)


# Register the adapters
gsm = getGlobalSiteManager()
gsm.registerAdapter(CheckboxRenderer, (ICheckboxWidget, Interface), IRenderer)
gsm.registerAdapter(CheckboxController, (ICheckboxWidget,), IWidgetController)
