from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.base.widget import Widget
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.widgets import ITextWidget
from zope.component import getGlobalSiteManager
from zope.interface import implementer, Interface


@implementer(ITextWidget)
class Text(Widget):
    """
    Text Widget. Representing a single read only string of characters that is broken into lines to float into the given space.
    """
    def handle_new_content(self, value):
        assert isinstance(value, str)
        super(Text, self).handle_new_content(value)


@implementer(IRenderer)
class TextRenderer(Renderer):
    """
    Renderer for a LinesWidget
    """
    __used_for__ = (ITextWidget, Interface)

    def render(self):
        pos_x = self.widget.pos_x
        pos_y = self.widget.pos_y

        if self.widget.width:
            width = self.widget.width
        else:
            width = self.display.width - pos_x

        content = self.widget.content
        start_pos = 0

        while True:
            rest_len = len(content[start_pos:])
            if width > rest_len:
                self.display.write_at_pos(pos_x, pos_y, content[start_pos:start_pos + width])
                break
            else:
                self.display.write_at_pos(pos_x, pos_y, content[start_pos:start_pos + width])
                start_pos += width
            pos_y += 1
        # return the coordinate after the content
        # ToDo width, height handling
        return pos_x, pos_y + 1


# Register the render adapter
gsm = getGlobalSiteManager()
gsm.registerAdapter(TextRenderer, (ITextWidget, Interface), IRenderer)
