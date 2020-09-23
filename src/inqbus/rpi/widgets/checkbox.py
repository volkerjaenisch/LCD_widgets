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
            out_str = self.special_chars['FOCUS_LEFT'] + \
                      content + \
                      self.special_chars['FOCUS_RIGHT']
        else:
            out_str = '[' + content + ']'
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



# Register the adapters
gsm = getGlobalSiteManager()
gsm.registerAdapter(ButtonRenderer, (IButtonWidget, Interface), IRenderer)
