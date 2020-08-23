from inqbus.rpi.widgets.base.widget import Widget
from inqbus.rpi.widgets.interfaces.widgets import (
    ILineWidget, ILinesWidget, ISelectWidget, IPageWidget, IButtonWidget, )

from inqbus.rpi.widgets.log import logging
from zope.interface import implementer


@implementer(ILineWidget)
class Line(Widget):

    def init_content(self):
        self._content = ''

    def clear_line(self, line_number=None):
        if line_number:
            self.display.set_cursor_pos = (line_number, 0)
        self.display.write_string(' ' * self.display.width)


@implementer(IButtonWidget)
class Button(Line):
    _click_handler = None

    def init_content(self):
        self._content = ''

    @property
    def click_handler(self):
        return self._click_handler

    @click_handler.setter
    def click_handler(self, handler):
        self._click_handler = handler


@implementer(ILinesWidget)
class Lines(Line):

    def init_content(self):
        self._content = []

    def handle_new_content(self, value):
        for line_val in value:
            if isinstance(line_val, str):
                line = Line()
                line.render_on_content_change = False
                line.content = line_val
                self._content.append(line)
            else:
                self._content.append(line_val)

        if self.render_on_content_change:
            self.render()


@implementer(ISelectWidget)
class Select(Lines):
    _selected_idx = 0
    render_on_selection_change = True

    @property
    def selected_idx(self):
        return self._selected_idx

    @selected_idx.setter
    def selected_idx(self, value):
        self._selected_idx = value
        if self.render_on_selection_change:
            self.render()


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
        self.selector.notify(signal)

    def notify(self, signal, value=None):
        logging.debug('Page received Signal: %s' % signal)
        target = self.active_widget
        if not target:
            return
        res = target.notify(signal)
        if res:
            return
        else:
            self.handle_signal(signal)

