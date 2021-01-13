import logging

from inqbus.rpi.widgets.base.render import Renderer, render_session
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.widgets import IPageWidget
from inqbus.rpi.widgets.select import Select
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(IPageWidget)
class Page(Select):
    selectable_widgets = []

    def add_widget(self, widget):
        widget.parent = self
        self.content.append(widget)

    def check_mark_selectable(self, widget):
        if widget.selectable:
            self.selectable_widgets.append(widget)

    def set_selectable(self, widget):
        if widget in self.selectable_widgets:
            return
        else:
            self.selectable_widgets = []
            for widget in self.content:
                self.check_mark_selectable(widget)

    @property
    def active_widget(self):
        if not self.selectable_widgets:
            return self.parent
        return self.selectable_widgets[0]

    def handle_signal(self, signal):
        self.selector.dispatch(signal)

    def notify(self, signal, value=None):
        logging.debug('Page received Signal: %s' % signal)
        target = self.active_widget
        if not target:
            return
        res = target.dispatch(signal)
        if res:
            return
        else:
            self.handle_signal(signal)


@implementer(IRenderer)
class PageRenderer(Renderer):
    __used_for__ = (IPageWidget, Interface)

    @render_session
    def render(self, pos_x=None, pos_y=None):
        """
        Render the Widget at a certain screen position
        Args:
            pos_x: horizontal display position
            pos_y: vertical display position

        """
        for widget in self.widget.content:
            if IPageWidget.providedBy(widget):
                a=5
            renderer = widget.render_for_display(self.display, pos_x=pos_x, pos_y=pos_y)
            pos_y = renderer.rendered_pos_y + 1
        # return the coordinate after the content
        # ToDo width, height handling


# Register the render adapter
gsm = getGlobalSiteManager()
gsm.registerAdapter(PageRenderer, (IPageWidget, Interface,), IRenderer)
