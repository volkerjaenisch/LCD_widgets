from inqbus.rpi.widgets.config_default import (
    FUCTION_CHARS_CURSES,
    FUNCTION_CHARS_LCD, CHAR_TRANSLATION_LCD, )
from inqbus.rpi.widgets.interfaces.widgets import IWidget
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.display import IDisplay, IRPLCD
from zope.interface import implementer
import zope.component


def render_session(original_function):
    def decorated(self, *args, **kwargs):
        self.display.open_session(self)
        result = original_function(self, *args, **kwargs)
        self.was_rendered = True
        self.display.commit_session(self)
        return result
    return decorated


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

        self.was_rendered = False
        self._rendered_width = None
        self._rendered_height = None
        self._rendered_pos_x = None
        self._rendered_pos_y = None

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
        self._rendered_pos_x = pos_x
        self._rendered_pos_y = pos_y

    def content(self):
        """
        Return the content of the Widget

        Returns:
            Content of the Widget
        """
        return self.widget.content

    @property
    def rendered_pos_x(self):
        """
        The rendered x position of the widget in screen coordinates
        """
        return self._rendered_pos_x

    @rendered_pos_x.setter
    def rendered_pos_x(self, value):
        """
        Set the horizontal render position of the widget

        Args:
            value: horizontal render position of the widget

        Returns:
            None
        """
        self._rendered_pos_x = value

    @property
    def rendered_pos_y(self):
        """
        The rendered_y position of the widget in screen coordinates
        """
        return self._rendered_pos_y

    @rendered_pos_y.setter
    def rendered_pos_y(self, value):
        """
        Set the vertical render position of the widget

        Args:
            value: vertical render position of the widget

        Returns:
            None
        """
        self._rendered_pos_y = value

    @property
    def rendered_width(self):
        """
        The rendered width of the widget in characters
        """
        if self._rendered_width is None:
            return self.widget._desired_width
        else:
            return self._rendered_width

    @rendered_width.setter
    def rendered_width(self, value):
        """
        Set the rendered width

        Args: value: new rendered width
        """
        self._rendered_width = value

    @property
    def rendered_height(self):
        """
        The rendered height of the widget in characters
        """
        if self._rendered_height is None:
            return self.widget._desired_height
        else:
            return self._rendered_height

    @rendered_height.setter
    def rendered_height(self, value):
        """
        Set the rendered height

        Args: value: new rendered height
        """
        self._rendered_height = value

    def render_position(self, pos_x, pos_y):
        if self.widget.fixed_pos:
            self.set_position(self.widget.pos_x, self.widget.pos_y)
        else:
            if pos_x is None:
                pos_x = 0
            if pos_y is None:
                pos_y = 0
            self.set_position(pos_x, pos_y)
        return self.rendered_pos_x, self.rendered_pos_y

    @render_session
    def render(self, pos_x=None, pos_y=None):
        """
        Render the Widget at a certain screen position
        Args:
            pos_x: horizontal display position
            pos_y: vertical display position

        Returns:
            the cursor position after rendering the widget
        """
        if self.widget.has_focus:
            if pos_y is not None:
                if (pos_y < 0 or pos_y > self.display.height-1):
                    if self.widget.parent.autoscroll:
                        result = self.widget.parent.render_for_display(display=self.display)
                        if result:
                            self.was_rendered = True
                        return result

            else:
                if self.rendered_pos_y is not None:
                    if self.rendered_pos_y < 0 or self.rendered_pos_y > self.display.height-1:
                        if self.widget.parent.autoscroll:
                            result = self.widget.parent.render_for_display(display=self.display)
                            if result:
                                self.was_rendered = True
                            return result

        self.clear()
        self.render_position(pos_x, pos_y)

        render_content = self.render_content()
        self.display.write_at_pos(
                self.rendered_pos_x,
                self.rendered_pos_y,
                render_content
        )
        self.rendered_width = len(render_content)
        self.was_rendered = True
        return self

    def render_focus(self, content):
        # If the widget is focussed
        # indicate this by changing its style
        if self.widget.has_focus:
            out_str = self.special_chars['FOCUS_LEFT'] + content
        else:
            out_str = ' ' + content
        return out_str

    def clear_focus(self, content):
        # If the widget is focussed
        # indicate this by changing its style
        out_str = ' ' + content
        return out_str


    def clear(self):
        """
        Render an Empty Widget at the current position of the widget
        """
        if not self.was_rendered:
            return

        self.display.erase_from_cleaning_mask(
                self.rendered_pos_x,
                self.rendered_pos_y,
                self.rendered_width
        )


gsm = zope.component.getGlobalSiteManager()
gsm.registerAdapter(Renderer, (IWidget, IDisplay), IRenderer)
