from inqbus.rpi.widgets.base.controller import WidgetController
from inqbus.rpi.widgets.interfaces.interfaces import IGUI, IMoveFocus
from zope.component import getGlobalSiteManager
from zope.interface import implementer


@implementer(IMoveFocus)
class MoveFocus(WidgetController):
    """
    This Adapter for WidgetControllers shifts the focus
    on a given WidgetController and relays the signal
    that causes the focus shift
    """

    __used_for__ = IGUI

    def __call__(self, signal):
        # Check if we obtain the focus
        assert self.widget.focus.has_focus is True
        # dispatch the signal
        self._signals[signal](signal)

    def on_click(self, signal):
        pass

    def on_up(self, signal):
        """
        Get the current focussed widget and shift
        the focus to the previous (sibling) widget
        :param signal:
        :return:
        """
        self.move_focus_to(self.widget.focus.prev_widget)

    def on_down(self, signal):
        """
        Get the current focussed widget and
        shift the focus to the next (sibling) widget
        :param signal:
        :return:
        """
        self.move_focus_to(self.widget.focus.next_widget)

    def move_focus_to(self, target_widget):
        """
        Move the focus to the object given
        :param target_widget: The object to focus on
        :return:
        """
        old_focus = self.widget.focus
        self.widget.focus = target_widget
        old_focus.render()
        # ToDo: This should be a signal send to the widget
        if target_widget:
            target_widget.render()


gsm = getGlobalSiteManager()
gsm.registerAdapter(MoveFocus, (IGUI,), IMoveFocus)
