from inqbus.rpi.widgets.base.widget import Widget, Selector
from inqbus.rpi.widgets.log import logging

class Line(Widget):

    def render(self):
        self.display.cursor_pos(*self.position)

        out_line = self.content
        out_line += (self.display.chars_per_line - len(self.content)) * ' '
        self.display.write(out_line)

    def clear_line(self, line_number=None):
        if line_number:
            self.display.cursor_pos = (line_number, 0)
        self.display.write_string(' ' * self.display.chars_per_line)


class Lines(Line):
    _content = []

    def __init__(self, position, line_count):
        super(Lines, self).__init__(position)
        self.line_count = line_count

    def render(self):
        y_pos, x_pos = self.position
        for line in self.content[0:self.line_count]:
            self.display.cursor_pos(y_pos, x_pos)
            y_pos += 1
            self.display.write(line)


class Select(Lines):
    _content = []
    _selectable = None

    def __init__(self, position, line_count):
        super(Lines, self).__init__(position)
        self.line_count = line_count
        self.selectable = True

    def handle_selectable(self, value):
        self.selectable = value

    def handle_new_content(self, value):
        super(Select, self).handle_new_content(value)

    def render(self):
        y_pos, x_pos = self.position
        for idx, line in enumerate(self.content[0:self.line_count]):
            self.display.cursor_pos(y_pos, x_pos)
            if idx == self.selector.selected_idx:
                self.display.write('>' + line)
            else:
                self.display.write(' ' + line)

            y_pos += 1


class Page(Widget):
    widgets = []
    selectable_widgets = []

    def __init__(self, controller, parent=None):
        super(Page, self).__init__((0,0))
        self.controller = controller
        self.display = controller.display
        self.parent = parent
        self._selector = Selector(self, self.selectable_widgets)

    def add_widget(self, widget):
        widget.display = self.display
        widget.parent = self
        self.widgets.append(widget)
        self.check_mark_selectable(widget)

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

    def render(self):
        for widget in self.widgets:
            widget.render()

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
