from inqbus.rpi.widgets.base.controller import WidgetController
from inqbus.rpi.widgets.interfaces.widgets import (
    IWidget, )
from inqbus.rpi.widgets.interfaces.interfaces import IMoveFocus, IGUI
from zope.component import getGlobalSiteManager
from zope.interface import implementer


@implementer(IMoveFocus)
class MoveFocus(WidgetController):
    __used_for__ = (IGUI)

    def __call__(self, signal):
        assert self.widget.focus.has_focus == True
        self._signals[signal](signal)

    def on_click(self, signal):
        pass

    def on_up(self, signal):
        self.update_focus(self.widget.focus.prev_widget)

    def on_down(self, signal):
        self.update_focus(self.widget.focus.next_widget)

    def update_focus(self, new_focus):
        old_focus = self.widget.focus
        self.widget.focus = new_focus
        old_focus.render()
        if new_focus:
            new_focus.render()


gsm = getGlobalSiteManager()
gsm.registerAdapter(MoveFocus, (IGUI,), IMoveFocus)
