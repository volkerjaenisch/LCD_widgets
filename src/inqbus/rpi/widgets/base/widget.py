from inqbus.rpi.widgets.interfaces.widgets import (
    IWidget, )
from inqbus.rpi.widgets.interfaces.interfaces import (
    IRenderer,
    IWidgetController, IGUI, )
from zope.component import getUtility, getMultiAdapter
from zope.interface import implementer


@implementer(IWidget)
class Widget(object):
    _content = None
    _parent = None
    _controller = None
    render_on_content_change = True
    autoscroll = False

    def __init__(self,
                 pos_x = 0,
                 pos_y = 0,
                 width=None,
                 height=None,
                 render_on_content_change=True,
                 autoscroll=True,
                 fixed_pos=False,
                 fixed_size=False,
                 ):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._width = width
        self._height = height
        fixed_pos = False,
        fixed_size = False,

        self.render_on_content_change = render_on_content_change
        self.autoscroll = autoscroll

        self._controller = IWidgetController(self)
        self.init_content()

    def init_content(self):
        pass

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self.handle_new_content(value)

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        self._pos_x = value

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, value):
        self._pos_y = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def prev_widget(self):
        return self._parent.get_prev_sibling(self)

    @property
    def next_widget(self):
        return self._parent.get_next_sibling(self)

    def get_prev_sibling(self, widget):
        widget_idx = self.content.index(widget)
        if widget_idx == 0:
            return self.parent
        return self.content[widget_idx - 1]

    def get_next_sibling(self, widget):
        widget_idx = self.content.index(widget)
        if widget_idx == len(self.content)-1 :
            return self.parent
        return self.content[widget_idx + 1]

    @property
    def length(self):
        return len(self.content)

    @property
    def height(self):
        if not self._height:
            return len(self._content)
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def width(self):
        if not self._width:
            return len(self._content)
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def controller(self):
        return self._controller

    @property
    def has_focus(self):
        gui = getUtility(IGUI)
        return gui.focus == self

    def render(self):
        gui = getUtility(IGUI)
        for display in gui.displays:
            renderer = getMultiAdapter((self, display), IRenderer)
            if renderer:
                renderer.render()

    def handle_new_content(self, value):
        self._content = value
        if self.render_on_content_change:
            self.render()

    def init(self):
        pass

