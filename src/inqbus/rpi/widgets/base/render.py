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

    def render(self):
        pass

gsm.registerAdapter(Renderer, (IWidget, IDisplay), IRenderer)
