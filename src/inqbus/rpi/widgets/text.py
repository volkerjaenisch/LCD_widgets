from inqbus.rpi.widgets.base.render import Renderer, render_session
from inqbus.rpi.widgets.base.widget import Widget
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.widgets import ITextWidget
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(ITextWidget)
class Text(Widget):
    """
    Text Widget. Representing a single read only string of characters.
    The content will be floating text filling the rectangle between
    the x,y pos of the widget and the boundaries given by width,
    height of the widget.
    If width and height are not given the display width/height
    will be used to constrain the content.
    If a text widget constrained by its own width/heigth will cross the
    display boundaries it will be clipped, but the text will not be broken
    at the boundary.
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

    @render_session
    def render(self, pos_x=None, pos_y=None):

        self.clear()
        pos_x, pos_y = self.render_position(pos_x, pos_y)

        if self.widget.width:
            width = self.widget.width
        else:
            width = self.display.width - pos_x

        content = self.widget.content
        start_pos_x = 0
        start_pos_y = pos_y
        while True:
            rest_len = len(content[start_pos_x:])
            if width > rest_len:
                self.display.write_at_pos(
                        pos_x,
                        pos_y,
                        content[start_pos_x:start_pos_x + width]
                )
                pos_y += 1
                break
            else:
                self.display.write_at_pos(
                        pos_x,
                        pos_y,
                        content[start_pos_x:start_pos_x + width]
                )
                start_pos_x += width
            pos_y += 1
        self.rendered_height = pos_y - start_pos_y
        self.rendered_width = width
        self.was_rendered = True
        # return the coordinate after the content
        return pos_x, pos_y + 1

    def clear(self):
        """
        Render empty Widget at the current position of the widget
        """
        if not self.was_rendered:
            return

        for pos_y in range(self.rendered_height):
            self.display.erase_from_cleaning_mask(
                self.rendered_pos_x,
                self.rendered_pos_y + pos_y,
                self.rendered_width
            )


# Register the render adapter
gsm = getGlobalSiteManager()
gsm.registerAdapter(TextRenderer, (ITextWidget, Interface), IRenderer)
