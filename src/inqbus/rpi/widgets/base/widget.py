from inqbus.rpi.widgets.interfaces.widgets import (
    IWidgetController, IRenderer,
    IGUI, IWidget, )
from zope.component import getUtility, getMultiAdapter
from zope.interface import implementer


@implementer(IWidget)
class Widget(object):
    _content = ''
    _parent = None
    _controller = None
    render_on_content_change = True
    autoscroll = False
    focused = False

    def __init__(self,
                 pos_x = 0,
                 pos_y = 0,
                 render_on_content_change=True,
                 autoscroll=True,
                 ):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.render_on_content_change = render_on_content_change
        self.autoscroll = autoscroll

        self._controller = IWidgetController(self)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self.handle_new_content(value)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def length(self):
        return len(self.content)

    @property
    def controller(self):
        return self._controller

    def render(self, pos_x=None, pos_y=None):
        if pos_x is None:
            pos_x = self.pos_x
        if pos_y is None:
            pos_y = self.pos_y
        gui = getUtility(IGUI)
        for display in gui.displays:
            renderer = getMultiAdapter((self, display), IRenderer)
            if renderer:
                renderer.render(pos_x=pos_x, pos_y=pos_y)

    def handle_new_content(self, value):
        self._content = value
        if self.render_on_content_change:
            self.render()

    def init(self):
        pass

