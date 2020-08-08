import logging

from inqbus.rpi.widgets.interfaces.widgets import IWidgetController, INotify
from zope.interface import implementer
from zope.component import getGlobalSiteManager


@implementer(INotify)
class Notify(object):
    __used_for__ = (IWidgetController,)
    def __init__(self, widget_controller):
        self.widget_controller = widget_controller

    def notify(self, signal):
        logging.debug('Signal received: ' + str(signal))
        logging.debug('Displatching signal :' + str(signal))
        logging.debug('Displatching signal to selectable ' + str(signal))
        result = self.widget_controller.notify(signal)
        return result

gsm = getGlobalSiteManager()
gsm.registerAdapter(Notify, (IWidgetController, ), INotify)
