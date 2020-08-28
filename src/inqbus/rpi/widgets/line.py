from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.base.widget import Widget
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.widgets import ILineWidget
from zope.component import getGlobalSiteManager
from zope.interface import implementer, Interface


@implementer(ILineWidget)
class Line(Widget):
    """
    Line Widget. Representing a single read only line of characters.
    """
    def handle_new_content(self, value):
        assert isinstance(value, str)
        super(Line, self).handle_new_content(value)

    def __init__(self, *args, **kwargs):
        super(Line, self).__init__(*args, **kwargs)
        self._desired_height = 1

    @property
    def width(self):
        """
        :return: the width of the widget in characters
        """
        if self._desired_width is None:
            return len(self.content)
        else:
            return self._desired_width

    @width.setter
    def width(self, value):
        """
        Set the width to a fixed value
        :param value: width
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
        :return: the new x, y position
        """
        # get the current widget position
        pos_x = self.widget.pos_x
        pos_y = self.widget.pos_y
        # issue the display to display the widgets content
        self.display.write_at_pos(pos_x, pos_y, self.widget.content)
        # return the coordinate after the content
        # ToDo width, height handling
        return pos_x, pos_y + 1


# Register the render adapter
gsm = getGlobalSiteManager()
gsm.registerAdapter(LineRenderer, (ILineWidget, Interface), IRenderer)
