from inqbus.rpi.widgets import events
from inqbus.rpi.widgets.base.events import event_registry
from inqbus.rpi.widgets.interfaces.widgets import (
    IWidgetController, IRenderer,
    IGUI, )
from inqbus.rpi.widgets.log import logging
from zope.component import getUtility, getMultiAdapter
from zope.interface import Interface




class Widget(object):
    _content = ''
    _parent = None
    _controller = None
    autorender = True
    autoscroll = False
    focused = False

    def __init__(self, position=None, **kwargs):
        if position:
            self.position = position
        else:
            self.position = (0,0)
        if 'autorender' in kwargs:
            self.autorender = kwargs['autorender']
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

    def render(self):
        gui = getUtility(IGUI)
        for display in gui.displays:
            renderer = getMultiAdapter((self, display), IRenderer)
            if renderer:
                renderer.render()

    def handle_new_content(self, value):
        self._content = value
        if self.autorender:
            self.render()

    def init(self):
        pass

