from inqbus.rpi.widgets.interfaces.widgets import (
    IRenderer, ILineWidget,
    IPageWidget, ISelectWidget, ILinesWidget, )
from inqbus.rpi.widgets.base.render import Renderer
from zope.component import getGlobalSiteManager
from zope.interface import implementer, Interface


@implementer(IRenderer)
class LineRenderer(Renderer):
    __used_for__ = (ILineWidget, Interface)
    def render(self):
        self.display.set_cursor_pos(*self.widget.position)
        out_line = self.widget.content
        out_line += (self.display.chars_per_line - len(self.widget.content)) * ' '
        self.display.write(out_line)


@implementer(IRenderer)
class LinesRenderer(Renderer):
    __used_for__ = (ILinesWidget,)

    def render(self):
        widget = self.widget
        y_pos, x_pos = widget.position
        for line in widget.content[0:widget.line_count]:
            self.display.set_cursor_pos(y_pos, x_pos)
            y_pos += 1
            self.display.write(line)


@implementer(IRenderer)
class SelectRenderer(Renderer):
    __used_for__ = (ISelectWidget,)

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
    __used_for__ = (IPageWidget,)

    def render(self):
        for widget in self.widget.widgets:
            IRenderer(widget).render()


gsm = getGlobalSiteManager()
gsm.registerAdapter(LineRenderer, (ILineWidget, Interface), IRenderer)
gsm.registerAdapter(LinesRenderer, (ILinesWidget, Interface,), IRenderer)
gsm.registerAdapter(LinesRenderer, (ISelectWidget, Interface,), IRenderer)
gsm.registerAdapter(LinesRenderer, (IPageWidget, Interface,), IRenderer)
