from inqbus.rpi.widgets.base import signals
from inqbus.rpi.widgets.base.log import logging
from inqbus.rpi.widgets.errors import SignalNotCatched
from inqbus.rpi.widgets.interfaces.interfaces import IWidgetController, IGUI
from inqbus.rpi.widgets.interfaces.widgets import IWidget
from zope.component import getGlobalSiteManager, getUtility
from zope.interface import implementer


@implementer(IWidgetController)
class WidgetController(object):
    """
    Each widget has a WidgetController assigned
    that takes care of all state changes:
    * Signal processing/dispatching
    * Changing the internal state of the Widget e.g.
        the selected index in a SelectWidget
    """
    __used_for__ = IWidget

    def __init__(self, widget):
        self.widget = widget
        self._signals = {
            signals.InputUp: self.on_up,
            signals.InputDown: self.on_down,
            signals.InputClick: self.on_click,
        }

    def on_click(self, signal):
        """
        Handles click signals

        Args:
            signal: incoming signal

        Returns:
            True if signal was handled, False otherwise
        """
        logging.debug(self.__class__.__name__ + ' done no click!')
        return False

    def on_down(self, signal):
        """
        Handles down signals

        Args:
            signal: incoming signal

        Returns:
            True if signal was handled, False otherwise
        """
        logging.debug(self.__class__.__name__ + ' done no Down')

        if self.widget.selected_idx < self.widget.length - 1:
            self.widget.selected_idx += 1
            return True
        else:
            return False

    def on_up(self, signal):
        """
        Handles up signals

        Args:
            signal: incoming signal

        Returns:
            True if signal was handled, False otherwise
        """
        logging.debug(self.__class__.__name__ + ' done Up')

        if self.widget.selected_idx > 0:
            self.widget.selected_idx -= 1
            return True
        else:
            return False

    def dispatch(self, signal):
        """
        Dispatches the incoming signal

        Args:
            signal: incoming signal
        Returns:
            True if signal was handled, False otherwise
        Raises:
            SignalNotCatched if signal could not be dispatched
        """
        result = self._signals[signal](signal)
        if result:
            return result
        else:
            if self.widget.parent is not None:
                return self.widget.parent.dispatch(signal)
            else:
                raise SignalNotCatched

    def acquire_focus(self):
        """
        Get the focus set on the widget. This can be on the widget the controller controlls
        or a subcompontent of the widget.
        Returns:
            True is a widget was found to focus on: False if not
        """
        if not self.widget._can_focus:
            return False

        self.set_as_focus(self.widget)

        return True

    def release_focus(self):
        """
        Release the focus set on this widget.
        Returns:
            True
        """
        self.widget.controller.set_as_focus(widget=None)
        self.widget.render()

    def set_as_focus(self, widget=None):
        """
        Set the controlled widget as focussed
        Args:
            widget:
        """
        gui = getUtility(IGUI)
        gui.focus = widget
        if widget is not None:
            widget.render()


gsm = getGlobalSiteManager()
gsm.registerAdapter(WidgetController, (IWidget,), IWidgetController)
