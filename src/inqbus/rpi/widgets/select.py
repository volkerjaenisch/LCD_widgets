import logging

from inqbus.rpi.widgets.base.controller import WidgetController
from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.interfaces.interfaces import (
    IRenderer,
    IWidgetController, )
from inqbus.rpi.widgets.interfaces.widgets import ISelectWidget
from inqbus.rpi.widgets.lines import Lines
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(ISelectWidget)
class Select(Lines):
    """
    The select widget
    """

    # knows its selected index
    _selected_idx = 0
    # and has a flag if it should be re-rendered
    # after a change of the selection index.
    # Usually the de-selected/selected items will render them selves
    # so this False by default. Use with care to much rendering can
    # cause severe side effects or slow down your application.
    render_on_selection_change = False
    # Automatically hold the focus in the display range
    autoscroll = True

    @property
    def selected_idx(self):
        """
        The current selected index
        """
        return self._selected_idx

    @selected_idx.setter
    def selected_idx(self, value):
        """
        Handles changes to the selected index

        Args: value: The new index
        """

        # store the new index
        self._selected_idx = value




@implementer(IRenderer)
class SelectRenderer(Renderer):
    __used_for__ = (ISelectWidget, Interface)

    def render(self, pos_x=None, pos_y=None):
        if pos_x is None:
            if self.widget.pos_x is not None:
                pos_x = self.widget.pos_x
            else:
                pos_x =0
        if pos_y is None:
            if self.widget.pos_y is not None:
                pos_y = self.widget.pos_y
            else:
                pos_y =0

        if self.widget.selected_idx + pos_y >= self.display.height:
            offset = (self.display.height - pos_y - 1)
            start_idx = self.widget.selected_idx - offset
            end_idx = self.widget.selected_idx + 1
        else:
            start_idx = 0
            end_idx = self.display.height - pos_y
        idx = start_idx
        for line in self.widget.content[start_idx:end_idx]:
            if self.widget.has_focus and idx == self.widget.selected_idx:
                self.display.write_at_pos(
                        pos_x,
                        pos_y,
                        self.special_chars['FOCUS_LEFT']
                )
            else:
                self.display.write_at_pos(pos_x, pos_y, ' ')
            idx += 1
        # return the coordinate after the content
        # ToDo width, height handling
        return pos_x, pos_y + 1


@implementer(IWidgetController)
class SelectController(WidgetController):
    """
    Each widget has a WidgetController assigned
    that takes care of all state changes:
    * Signal processing/dispatching
    * Changing the internal state of the Widget e.g.
        the selected index in a SelectWidget
    """
    __used_for__ = ISelectWidget

    def on_down(self, signal):
        """
        Handles down signals

        Args:
            signal: incoming signal

        Returns:
            True if signal was handled, False otherwise
        """
        logging.debug(self.__class__.__name__ + ' doing Down')

        new_idx = self.next_focusable_widget_idx_down()
        if new_idx is None:
            return False

        # store the new index into the widget
        self.widget.selected_idx = self.change_focus(
                self.widget.selected_idx,
                new_idx
        )
        logging.debug(self.__class__.__name__ + ' done Down')
        return True


    def on_up(self, signal):
        """
        Handles up signals

        Args:
            signal: incoming signal

        Returns:
            True if signal was handled, False otherwise
        """
        logging.debug(self.__class__.__name__ + ' doing Up')

        new_idx = self.next_focusable_widget_idx_up()
        if new_idx is None:
            return False
        # store the new index into the widget
        self.widget.selected_idx = self.change_focus(
                self.widget.selected_idx,
                new_idx
        )
        logging.debug(self.__class__.__name__ + ' done Up')
        return True

    def next_focusable_widget_idx_up(self):
        result = None
        if self.widget.selected_idx-1 < 0:
            return result
        for idx in range(self.widget.selected_idx-1, -1, -1):
            if self.widget._content[idx]._can_focus:
                result = idx
                break
        return result

    def next_focusable_widget_idx_down(self):
        result = None
        if self.widget.selected_idx+1 > self.widget.length-1:
            return result
        for idx in range(self.widget.selected_idx+1, self.widget.length ):
            if self.widget._content[idx]._can_focus:
                result = idx
                break
        return result


    def change_focus(self, old_focus_idx, new_focus_idx):
        # Remember old selection index
        old_focussed_widget = self.widget.content[old_focus_idx]
        # The new focus
        new_focussed_widget = self.widget.content[new_focus_idx]
        # Shift the focus to the new widget. Since the focus is global,
        # a widget cannot render itself without focus while be having the
        # focus pointing to it.
        self.widget.controller.set_as_focus(new_focussed_widget)

        # Let the old focussed widget release the focus (Render itself)
        old_focussed_widget.controller.release_focus()
        # Let the new focussed widget acquire the focus (Render itself)
        new_focussed_widget.controller.acquire_focus()

        return new_focus_idx

    def acquire_focus(self):
        """
        Get the focus set on the widget. This can be on the widget the controller controlls
        or a subcompontent of the widget.
        Returns:
            True is a widget was found to focus on: False if not
        """
        result = False
        new_idx = self.next_focusable_widget_idx_down()
        if new_idx is None :
            return result
        result = self.widget._content[new_idx].controller.acquire_focus()
        self.widget.selected_idx = new_idx
        return True

# Register the render adapter
gsm = getGlobalSiteManager()
gsm.registerAdapter(SelectRenderer, (ISelectWidget, Interface,), IRenderer)
gsm.registerAdapter(SelectController, (ISelectWidget,), IWidgetController)
