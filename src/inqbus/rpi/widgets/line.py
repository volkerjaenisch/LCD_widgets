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

    def render_content(self):
        """
        Render the line content

        """

        return self.widget.content


# Register the render adapter
gsm = getGlobalSiteManager()
gsm.registerAdapter(LineRenderer, (ILineWidget, Interface), IRenderer)
