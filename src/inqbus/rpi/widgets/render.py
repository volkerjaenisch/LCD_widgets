from inqbus.rpi.widgets.interfaces.widgets import (
    IRenderer, ILineWidget,
    IPageWidget, ISelectWidget, ILinesWidget, IButtonWidget, )
from inqbus.rpi.widgets.base.render import Renderer
from zope.component import getGlobalSiteManager
from zope.interface import implementer, Interface


@implementer(IRenderer)
class LineRenderer(Renderer):
    __used_for__ = (ILineWidget, Interface)
    def render(self, pos_x=None, pos_y=None):
        super(LineRenderer, self).render(pos_x=pos_x, pos_y=pos_y)
        self.display.write_at_pos(pos_x, pos_y, self.widget.content)
        return pos_x, pos_y + 1


@implementer(IRenderer)
class ButtonRenderer(Renderer):
    __used_for__ = (IButtonWidget, Interface)
    def render(self, pos_x=None, pos_y=None):
        super(ButtonRenderer, self).render(pos_x=pos_x, pos_y=pos_y)
        if self.widget.has_focus:
            self.display.write_at_pos(pos_x, pos_y, '>')
            self.display.write_at_pos(pos_x + 1, pos_y, self.widget.content)
            self.display.write_at_pos(pos_x + len(self.widget.content), pos_y, '<')
        else:
            self.display.write_at_pos(pos_x, pos_y, '[')
            self.display.write_at_pos(pos_x + 1, pos_y, self.widget.content)
            self.display.write_at_pos(pos_x + len(self.widget.content), pos_y, ']')

        return pos_x, pos_y + 1


@implementer(IRenderer)
class LinesRenderer(Renderer):
    __used_for__ = (ILinesWidget,)

    def render(self, pos_x=None, pos_y=None):
        super(LinesRenderer, self).render(pos_x=pos_x, pos_y=pos_y)
        pos_x = self.pos_x
        pos_y = self.pos_y
        if self.widget.height == 1:
            _pos_x, pos_y = self.get_display_renderer_for(self.widget.content[0]).render(
                    pos_x,
                    pos_y
            )
        else:
            self.display.write_at_pos(pos_x, pos_y, '/')
            _pos_x, pos_y = self.get_display_renderer_for(self.widget.content[0]).render(
                    pos_x + 1,
                    pos_y
            )
            for line in self.widget.content[1:self.widget.height - 1]:
                self.display.write_at_pos(pos_x, pos_y, '|')
                _pos_x, pos_y = self.get_display_renderer_for(line).render(pos_x + 1, pos_y)
            self.display.write_at_pos(pos_x, pos_y, chr(0b01100000))
            _pos_x, pos_y = self.get_display_renderer_for(self.widget.content[self.widget.height-1]).render(
                    pos_x + 1,
                    pos_y
            )

        return pos_x, pos_y


@implementer(IRenderer)
class SelectRenderer(Renderer):
    __used_for__ = (ISelectWidget,)

    def render(self, pos_x=None, pos_y=None):
        super(SelectRenderer, self).render(pos_x=pos_x, pos_y=pos_y)
        pos_x = self.pos_x
        pos_y = self.pos_y

        if self.widget.selected_idx + pos_y >= self.display.height:
            start_idx =  self.widget.selected_idx - (self.display.height - pos_y - 1)
            end_idx = self.widget.selected_idx + 1
        else:
            start_idx = 0
            end_idx = self.display.height - pos_y
        idx = start_idx
        for line in self.widget.content[start_idx:end_idx]:
            if self.widget.has_focus and idx == self.widget.selected_idx :
                    self.display.write_at_pos(pos_x, pos_y, '>')
            else:
                self.display.write_at_pos(pos_x, pos_y, ' ')
            _pos_x, pos_y = self.get_display_renderer_for(line).render(pos_x+1, pos_y)
            idx += 1
        return pos_x, pos_y


@implementer(IRenderer)
class PageRenderer(Renderer):
    __used_for__ = (IPageWidget,)

    def render(self, pos_x=None, pos_y=None):
        for widget in self.widget.content:
            widget.render()


gsm = getGlobalSiteManager()
gsm.registerAdapter(LineRenderer, (ILineWidget, Interface), IRenderer)
gsm.registerAdapter(ButtonRenderer, (IButtonWidget, Interface), IRenderer)
gsm.registerAdapter(LinesRenderer, (ILinesWidget, Interface,), IRenderer)
gsm.registerAdapter(SelectRenderer, (ISelectWidget, Interface,), IRenderer)
gsm.registerAdapter(PageRenderer, (IPageWidget, Interface,), IRenderer)
