import logging

from inqbus.rpi.widgets import events
from inqbus.rpi.widgets.errors import SignalNotCatched
from zope.component import getGlobalSiteManager
from inqbus.rpi.widgets.interfaces.widgets import IWidgetController, IWidget
from zope.interface import implementer


@implementer(IWidgetController)
class WidgetController(object):
    __used_for__ = (IWidget)
    _active_page = None

    def __init__(self, widget):
        self.widget = widget
        self.modules = []
        self._events = {
            events.Input_Up: self.on_up,
            events.Input_Down: self.on_down,
            events.Input_Click: self.on_click,
        }

    @property
    def active_page(self):
        return self._active_page

    @active_page.setter
    def active_page(self, value):
        self._active_page = value
        self._active_page.render()

    def register_module(self, module):
        self.modules.append(module(self))

    def on_click(self, signal):
        logging.debug(self.__class__.__name__ + ' done click')
        return True

    def on_down(self, signal):
        logging.debug(self.__class__.__name__ + ' done Down')
        #        import pdb; pdb.set_trace()

        if self.widget.selected_idx < self.widget.length - 1:
            self.widget.selected_idx += 1
            return True
        else:
            return False

    def on_up(self, signal):
        logging.debug(self.__class__.__name__ + ' done Up')
        #        import pdb; pdb.set_trace()
        if self.widget.selected_idx > 0:
            self.widget.selected_idx -= 1
            return True
        else:
            return False

    def notify(self, signal):
        result = self._events[signal](signal)
        if result:
            return result
        else:
            if self.widget.parent:
                return self.widget.parent.notify(signal)
            else:
                raise SignalNotCatched



gsm = getGlobalSiteManager()
gsm.registerAdapter(WidgetController, (IWidget,), IWidgetController)

