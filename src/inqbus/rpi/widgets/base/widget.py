from inqbus.rpi.widgets import events
from inqbus.rpi.widgets.base.events import event_registry
from inqbus.rpi.widgets.interfaces.widgets import IWidgetController
from inqbus.rpi.widgets.log import logging


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
    def controller(self):
        return self._controller

    def render(self):
        pass

    def handle_new_content(self, value):
        self._content = value
        if self.autorender:
            self.render()
        if self._controller:
            self._controller.select_on = self.content

