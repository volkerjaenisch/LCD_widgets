from inqbus.rpi.widgets.base.widget import Widget
from inqbus.rpi.widgets.interfaces.widgets import (
    IWidgetController,
    ILineWidget, ILinesWidget, ISelectWidget, IPageWidget, )
from inqbus.rpi.widgets.log import logging
from zope.interface import implementer


@implementer(ILineWidget)
class Line(Widget):

    def clear_line(self, line_number=None):
        if line_number:
            self.display.set_cursor_pos = (line_number, 0)
        self.display.write_string(' ' * self.display.chars_per_line)


@implementer(ILinesWidget)
class Lines(Line):
    _content = None

    def __init__(self, position, line_count):
        super(Lines, self).__init__(position)
        self._content = []
        self.line_count = line_count


@implementer(ISelectWidget)
class Select(Lines):
    _content = None
    selected_idx = 0


    def handle_new_content(self, value):
        super(Select, self).handle_new_content(value)




@implementer(IPageWidget)
class Page(Select):
    widgets = []
    selectable_widgets = []

    def add_widget(self, widget):
        widget.parent = self
        self.widgets.append(widget)
#        self.check_mark_selectable(widget)

    def check_mark_selectable(self, widget):
        if widget.selectable:
            self.selectable_widgets.append(widget)

    def set_selectable(self, widget):
        if widget in self.selectable_widgets:
            return
        else:
            self.selectable_widgets = []
            for widget in self.widgets:
                self.check_mark_selectable(widget)

    def active_widget(self):
        if not self.selectable_widgets:
            return None
        return self.selectable_widgets[0]


    def handle_signal(self, signal):
        self.selector.notify(signal)

    def notify(self, signal, value=None):
        logging.debug('Page received Signal: ' + signal)
        target = self.active_widget()
        if not target:
            return
        res = target.notify(signal)
        if res:
            return
        else:
            self.handle_signal(signal)
