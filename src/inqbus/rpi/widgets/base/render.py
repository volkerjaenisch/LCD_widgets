from inqbus.rpi.widgets.interfaces.widgets import IWidget
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.component import getMultiAdapter
from zope.interface import implementer
import zope.component

gsm = zope.component.getGlobalSiteManager()

@implementer(IRenderer)
class Renderer(object):
    """
    The Renderer is a multiadapter for a given widget and frame_buffer combination.
    It handles therefore two things:
        * the visual appearance of the widget.
        * and its appearance on a certain type of Display. A potential Display may be character frame_buffer, or HTML file...
    """
    __used_for__ = (IWidget, IDisplay)

    def __init__(self, widget, display):
        self.widget = widget
        self.display = display

    def set_position(self, pos_x, pos_y):
        """
        Set the position of the widget in frame_buffer coordinates
        :param pos_x:
        :param pos_y:
        :return:
        """
        self.widget.pos_x = pos_x
        self.widget.pos_y = pos_y

    def content(self):
        """
        Return the content of the Widget
        :return:
        """
        return self.widget.content

    def render(self):
        """
        Render the Widget
        :return: the cursor position after rendering the widget
        """
        return self.widget.pos_x, self.widget.pos_y

    def render_at(self, pos_x, pos_y):
        """
        Render the Widget at a certain screen position
        :param pos_x:
        :param pos_y:
        :return: the cursor position after rendering the widget
        """
        self.set_position(pos_x, pos_y)
        return self.render()

    def clear(self):
        """
        Render an Empty Widget at the current position of the widget
        :return: the cursor position after rendering the widget
        """
        self.display.write_at_pos(self.widget.pos_x, self.widget.pos_y, ' ' * self.widget.length)
        return self.widget.pos_x, self.widget.pos_y

    def get_display_renderer_for(self, widget):
        """
        Helper function to retrieve the renderer multiadapter for a given widget
        :param widget:
        :return:
        """
        renderer = getMultiAdapter((widget, self.display), IRenderer)
        return renderer


gsm.registerAdapter(Renderer, (IWidget, IDisplay), IRenderer)
