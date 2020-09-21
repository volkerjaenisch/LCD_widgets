from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.base.widget import Widget
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.widgets import ILineWidget
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(ILineWidget)
class Line(Widget):
    """
    Line Widget. Representing a single read only line of characters.
    """
    def handle_new_content(self, value):
        """
        Handle new content to the widget

        Args:
            value: THe new content
        """
        assert isinstance(value, str)
        super(Line, self).handle_new_content(value)

    def __init__(self, *args, **kwargs):
        super(Line, self).__init__(*args, **kwargs)
        self._desired_height = 1

    @property
    def width(self):
        """
        The width of the widget in characters
        """
        if self._desired_width is None:
            return len(self.content)
        else:
            return self._desired_width

    @width.setter
    def width(self, value):
        """
        Set the width to a fixed value

        Args: value: width
        """
        self._desired_width = value


@implementer(IRenderer)
class LineRenderer(Renderer):
    """
    Renderer for a LineWidget
    """
    __used_for__ = (ILineWidget, Interface)

    def render(self):
        """
        Render the line at the given position

        Returns:
            the new x, y position
        """

        # get the current widget position
        pos_x = self.rendered_pos_x
        pos_y = self.rendered_pos_y
        # check if we have something to render
        if self.widget.content is None:
            # .. if not simply return our original coordinates
            return pos_x, pos_y

        content = self.render_clear(self.widget.content)
        # issue the frame_buffer to frame_buffer the widgets content
        self.display.write_at_pos(pos_x, pos_y, content)
        # return the coordinate after the content
        # ToDo width, height handling
        return pos_x, pos_y + 1


# Register the render adapter
gsm = getGlobalSiteManager()
gsm.registerAdapter(LineRenderer, (ILineWidget, Interface), IRenderer)
