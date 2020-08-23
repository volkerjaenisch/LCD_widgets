from inqbus.rpi.widgets.interfaces.widgets import IWidget
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.component import getMultiAdapter
from zope.interface import implementer
import zope.component

gsm = zope.component.getGlobalSiteManager()

@implementer(IRenderer)
class Renderer(object):
    __used_for__ = (IWidget, IDisplay)

    def __init__(self, widget, display):
        self.widget = widget
        self.display = display

    def set_position(self, pos_x, pos_y):
        self.widget.pos_x = pos_x
        self.widget.pos_y = pos_y

    def render(self):
        return self.widget.pos_x, self.widget.pos_y

    def render_at(self, pos_x, pos_y):
        self.set_position(pos_x, pos_y)
        return self.render()

    def clear(self):
        self.display.write_at_pos(self.widget.pos_x, self.widget.pos_y, ' ' * self.widget.length)

    def get_display_renderer_for(self, widget):
        renderer = getMultiAdapter((widget, self.display), IRenderer)
        return renderer


gsm.registerAdapter(Renderer, (IWidget, IDisplay), IRenderer)
