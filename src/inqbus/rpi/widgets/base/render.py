from inqbus.rpi.widgets.config_default import (
    FUCTION_CHARS_CURSES,
    FUNCTION_CHARS_LCD, CHARMAP_LCD, CHAR_TRANSLATION_LCD, )
from inqbus.rpi.widgets.interfaces.widgets import IWidget
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.display import IDisplay, IRPLCD
from zope.component import getMultiAdapter
from zope.interface import implementer
import zope.component


@implementer(IRenderer)
class Renderer(object):
    """
    The Renderer is a multi adapter for a given
    widget and display combination.
    It handles therefore two things:
        * the visual appearance of the widget.
        * and its appearance on a certain type of Display. A display
            may be character frame_buffer, or HTML file...
    """

    __used_for__ = (IWidget, IDisplay)

    def __init__(self, widget, display):
        self.widget = widget
        self.display = display

        if IRPLCD.providedBy(self.display):
            self.special_chars = FUNCTION_CHARS_LCD
            self.char_translation = CHAR_TRANSLATION_LCD
        else:
            self.special_chars = FUCTION_CHARS_CURSES
            self.char_translation = None

    def set_position(self, pos_x, pos_y):
        """
        Set the position of the widget in frame_buffer coordinates

        Args:
            pos_x: horizontal display position
            pos_y: vertical display position

        Returns:
            None
        """
        self.widget.pos_x = pos_x
        self.widget.pos_y = pos_y

    def content(self):
        """
        Return the content of the Widget

        Returns:
            Content of the Widget
        """
        return self.widget.content

    def render(self):
        """
        Render the Widget

        Returns:
            the cursor position after rendering the widget
        """
        return self.widget.pos_x, self.widget.pos_y

    def render_at(self, pos_x, pos_y):
        """
        Render the Widget at a certain screen position
        Args:
            pos_x: horizontal display position
            pos_y: vertical display position

        Returns: the cursor position after rendering the widget
        """
        if self.widget.fixed_pos:
            self.set_position(self.widget.pos_x, self.widget.pos_y)
        else:
            self.set_position(pos_x, pos_y)
        return self.render()

    def render_focus(self, content):
        # If the button is focussed
        # indicate this by changing the braces to angles
        if self.widget.has_focus:
            out_str = self.special_chars['FOCUS_LEFT'] + content
        else:
            out_str = ' ' + content
        return out_str

    def render_clear(self, content):
        # Render and clear the former content from the display.
        # also set the new rendered width.
        result = content
        if self.widget.rendered_width is not None and self.widget.rendered_width > len(content):
            result = content + ' ' * (self.widget.rendered_width-len(content))

        self.widget.rendered_width = len(content)
        return result

    def clear(self):
        """
        Render an Empty Widget at the current position of the widget

        Returns: the cursor position after rendering the widget
        """
        self.display.write_at_pos(
                self.widget.pos_x,
                self.widget.pos_y,
                ' ' * self.widget.rendered_width
        )
        return self.widget.pos_x, self.widget.pos_y

    def get_display_renderer_for(self, widget):
        """
        Helper function to retrieve the renderer multi adapter
        for a given widget

        Args:
            widget:
                The display a renderer has to be supplied for

        Returns:
            None
        """
        renderer = getMultiAdapter((widget, self.display), IRenderer)
        return renderer


gsm = zope.component.getGlobalSiteManager()
gsm.registerAdapter(Renderer, (IWidget, IDisplay), IRenderer)
