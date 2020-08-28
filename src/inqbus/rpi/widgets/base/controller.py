from inqbus.rpi.widgets.base.log import logging

from inqbus.rpi.widgets.base import signals
from inqbus.rpi.widgets.errors import SignalNotCatched
from zope.component import getGlobalSiteManager
from inqbus.rpi.widgets.interfaces.widgets import IWidget
from inqbus.rpi.widgets.interfaces.interfaces import IWidgetController
from zope.interface import implementer


@implementer(IWidgetController)
class WidgetController(object):
    """
    Each widget has a WidgetController assigned that takes care of all state changes:
    * Signal processing/dispatching
    * Changing the internal state of the Widget e.g. the selected index in a SelectWidget
    """
    __used_for__ = (IWidget)

    def __init__(self, widget):
        self.widget = widget
        self._signals = {
            signals.Input_Up: self.on_up,
            signals.Input_Down: self.on_down,
            signals.Input_Click: self.on_click,
        }

    def on_click(self, signal):
        logging.debug(self.__class__.__name__ + ' done click')
        return True

    def on_down(self, signal):
        logging.debug(self.__class__.__name__ + ' done Down')

        if self.widget.selected_idx < self.widget.length - 1:
            self.widget.selected_idx += 1
            return True
        else:
            return False

    def on_up(self, signal):
        logging.debug(self.__class__.__name__ + ' done Up')

        if self.widget.selected_idx > 0:
            self.widget.selected_idx -= 1
            return True
        else:
            return False

    def notify(self, signal):
        result = self._signals[signal](signal)
        if result:
            self.widget.render()
            return result
        else:
            if self.widget.parent:
                return self.widget.parent.notify(signal)
            else:
                raise SignalNotCatched


gsm = getGlobalSiteManager()
gsm.registerAdapter(WidgetController, (IWidget,), IWidgetController)

