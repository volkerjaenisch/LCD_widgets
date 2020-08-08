from inqbus.rpi.widgets.interfaces.widgets import IRenderer
from inqbus.rpi.widgets.base.render import Renderer
from zope.interface import implementer

@implementer(IRenderer)
class LineRenderer(Renderer):

    def render(self):
        self.display.set_cursor_pos(*self.widget.position)
        out_line = self.widget.content
        out_line += (self.display.chars_per_line - len(self.widget.content)) * ' '
        self.display.write(out_line)


@implementer(IRenderer)
class LinesRenderer(Renderer):

    def render(self):
        widget = self.widget
        y_pos, x_pos = widget.position
        for line in widget.content[0:widget.line_count]:
            self.display.set_cursor_pos(y_pos, x_pos)
            y_pos += 1
            self.display.write(line)


@implementer(IRenderer)
class SelectRenderer(Renderer):

    def render(self):
        y_pos, x_pos = self.widget.position
        for idx, line in enumerate(self.content[0:self.line_count]):
            self.display.set_cursor_pos(y_pos, x_pos)
            if idx == self.selector.selected_idx:
                self.display.write('>' + line)
            else:
                self.display.write(' ' + line)
            y_pos += 1


@implementer(IRenderer)
class PageRenderer(Renderer):

    def render(self):
        for widget in self.widget.widgets:
            IRenderer(widget).render()
