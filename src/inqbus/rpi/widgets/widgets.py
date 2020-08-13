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

    def __init__(self, pos_x=0, pos_y=0, line_count=None):
        super(Lines, self).__init__(pos_x=pos_x, pos_y=pos_y)
        self._content = []
        self.line_count = line_count


@implementer(ISelectWidget)
class Select(Lines):
    _content = None
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

    def handle_new_content(self, value):
        for line_val in value:
            if isinstance(line_val, str):
                line = Line()
                line.render_on_content_change = False
                line.content = line_val
                self._content.append(line)
        if self.render_on_content_change:
            self.render()


@implementer(IPageWidget)
class Page(Select):
    widgets = []
    selectable_widgets = []

    def add_widget(self, widget):
        widget.parent = self
        self.widgets.append(widget)

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

    @property
    def length(self):
        return len(self.widgets)

