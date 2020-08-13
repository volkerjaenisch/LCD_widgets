from inqbus.rpi.widgets.interfaces.widgets import (
    IWidgetController, IPageWidget, )
from zope.interface import implementer


@implementer(IWidgetController)
class PageController(object):
    __used_for__ = (IPageWidget)

    def notify(self, signal):
        result = self.widget.active_widget.notify(signal)


