from inqbus.rpi.widgets.base.controller import WidgetController
from inqbus.rpi.widgets.interfaces.widgets import (
    IWidgetController, IPageWidget, IButtonWidget, INotify, )
from inqbus.rpi.widgets.signals import Input_Click
from zope.component import getGlobalSiteManager
from zope.interface import implementer



@implementer(IWidgetController)
class ButtonController(WidgetController):
    __used_for__ = (IButtonWidget)

    def notify(self, signal):
        if signal == Input_Click:
            return self.widget.click_handler()
        else:
            return False

@implementer(IWidgetController)
class PageController(WidgetController):
    __used_for__ = (IPageWidget)

    def notify(self, signal):
        notifier = INotify(self.widget.active_widget.controller)
        result = notifier.notify(signal)
        return result


gsm = getGlobalSiteManager()
gsm.registerAdapter(ButtonController, (IButtonWidget,), IWidgetController)
gsm.registerAdapter(PageController, (IPageWidget,), IWidgetController)
