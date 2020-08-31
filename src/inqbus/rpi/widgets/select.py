from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.widgets import ISelectWidget
from inqbus.rpi.widgets.lines import Lines
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(ISelectWidget)
class Select(Lines):
    """
    The select widget
    """
    # knows it selected index
    _selected_idx = 0
    # and has a flag if it should be rendered
    # after a change of the selcetion index
    render_on_selection_change = True

    @property
    def selected_idx(self):
        """
        :return: The current selected index
        """
        return self._selected_idx

    @selected_idx.setter
    def selected_idx(self, value):
        """
        Handles changes to the selected index
        :param value: the new index
        :return:
        """
        # store the new index
        self._selected_idx = value
        # if render_on_selection_change is set ..
        if self.render_on_selection_change:
            # .. render the widget
            self.render()


@implementer(IRenderer)
class SelectRenderer(Renderer):
    __used_for__ = (ISelectWidget, Interface)

    def render(self):
        pos_x = self.widget.pos_x
        pos_y = self.widget.pos_y

        if self.widget.selected_idx + pos_y >= self.display.height:
            offset = (self.display.height - pos_y - 1)
            start_idx =  self.widget.selected_idx - offset
            end_idx = self.widget.selected_idx + 1
        else:
            start_idx = 0
            end_idx = self.display.height - pos_y
        idx = start_idx
        for line in self.widget.content[start_idx:end_idx]:
            if self.widget.has_focus and idx == self.widget.selected_idx:
                self.display.write_at_pos(pos_x, pos_y, '>')
            else:
                self.display.write_at_pos(pos_x, pos_y, ' ')
            renderer = self.get_display_renderer_for(line)
            _pos_x, pos_y = renderer.render_at(pos_x+1, pos_y)
            idx += 1
        # return the coordinate after the content
        # ToDo width, height handling
        return pos_x, pos_y + 1


# Register the render adapter
gsm = getGlobalSiteManager()
gsm.registerAdapter(SelectRenderer, (ISelectWidget, Interface,), IRenderer)
