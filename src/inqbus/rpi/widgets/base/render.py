from inqbus.rpi.widgets.interfaces.widgets import IWidget, IRenderer, IDisplay
from zope.interface import implementer
import zope.component

gsm = zope.component.getGlobalSiteManager()

@implementer(IRenderer)
class Renderer(object):
    __used_for__ = (IWidget, IDisplay)

    def __init__(self, widget, display):
        self.widget = widget
        self.display = display

    def render(self, pos_x=None, pos_y=None):
        if pos_x is None:
            self.pos_x = self.widget.pos_x
        else:
            self.pos_x = pos_x

        if pos_y is None:
            self.pos_y = self.widget.pos_y
        else:
            self.pos_y = pos_y

gsm.registerAdapter(Renderer, (IWidget, IDisplay), IRenderer)
