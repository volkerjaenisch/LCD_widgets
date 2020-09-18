from inqbus.rpi.widgets.interfaces.widgets import (
    IWidget, )
from inqbus.rpi.widgets.interfaces.interfaces import (
    IRenderer,
    IWidgetController, IGUI, )
from zope.component import getUtility, getMultiAdapter
from zope.interface import implementer


@implementer(IWidget)
class Widget(object):
    """
    Base class for all widgets. The widget classes contains
    no functionality but only the state of the widget.
    That is the content, position, dimensions, and parameters.
    Functionality is provided by adapters e.g. for rendering,
    visual effects, focus change, signal handling.
    """

    _content = None
    _parent = None
    _controller = None
    render_on_content_change = True
    render_on_focus_change = True
    autoscroll = False

    def __init__(self,
                 pos_x = 0,
                 pos_y = 0,
                 width=None,
                 height=None,
                 render_on_content_change=True,
                 autoscroll=True,
                 fixed_pos=False,
                 fixed_size=False,
                 ):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._desired_width = width
        self._desired_height = height
        self._rendered_width = None
        self._rendered_height = None

        self.fixed_pos = fixed_pos
        self.fixed_size = fixed_size

        self.render_on_content_change = render_on_content_change
        self.autoscroll = autoscroll

        self._controller = IWidgetController(self)
        self.init_content()

    def init_content(self):
        """
        Hook for content initialisation

        Returns:
            None
        """
        pass

    @property
    def content(self):
        """
        The content of the widget. This may be a simple string value or a
        more complex content like other widgets or a list of other widgets.

        Returns:
            None
        """
        return self._content

    @content.setter
    def content(self, value):
        """
        The content setter is responsible for the handling
        of new context. This is especially useful if content changes
        during the program run.

        Args:
            value:
                The content of the widget

        Returns:
            None
        """
        self.handle_new_content(value)

    @property
    def pos_x(self):
        """
        The x position of the widget in screen coordinates
        """
        return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        """
        Set the horizontal position of the widget

        Args:
            value: horizontal position of the widget
        """
        self._pos_x = value

    @property
    def pos_y(self):
        """
        The y position of the widget in screen coordinates
        """
        return self._pos_y

    @pos_y.setter
    def pos_y(self, value):
        """
        Set the vertical position of the widget

        Args:
            value: vertical position of the widget

        Returns:
            None
        """
        self._pos_y = value

    @property
    def rendered_pos_x(self):
        """
        The rendered x position of the widget in screen coordinates
        """
        if self.rendered__pos_x is None:
            return self.pos_x
        else:
            return self.rendered__pos_x

    @rendered_pos_x.setter
    def rendered_pos_x(self, value):
        """
        Set the horizontal render position of the widget

        Args:
            value: horizontal render position of the widget

        Returns:
            None
        """
        self.rendered__pos_x = value

    @property
    def rendered_pos_y(self):
        """
        The rendered_y position of the widget in screen coordinates
        """
        if self.rendered__pos_y is None:
            return self.pos_y
        else:
            return self.rendered__pos_y

    @rendered_pos_y.setter
    def rendered_pos_y(self, value):
        """
        Set the vertical render position of the widget

        Args:
            value: vertical render position of the widget

        Returns:
            None
        """
        self.rendered__pos_y = value

    @property
    def height(self):
        """
        The height of the widget in characters
        """
        return self._desired_height

    @height.setter
    def height(self, value):
        """
        Set the height to a fixed value

        Args: value: height
        """
        self._desired_height = value

    @property
    def width(self):
        """
        The width of the widget in characters
        """
        return self._desired_width

    @width.setter
    def width(self, value):
        """
        Set the width to a fixed value

        Args: value: width
        """
        self._desired_width = value

    @property
    def rendered_width(self):
        """
        The rendered width of the widget in characters
        """
        if self._rendered_width is None:
            return self._desired_width
        else:
            return self._rendered_width

    @rendered_width.setter
    def rendered_width(self, value):
        """
        Set the rendered width

        Args: value: new rendered width
        """
        self._rendered_width = value

    @property
    def rendered_height(self):
        """
        The rendered height of the widget in characters
        """
        if self._rendered_height is None:
            return self._desired_height
        else:
            return self._rendered_height

    @rendered_height.setter
    def rendered_height(self, value):
        """
        Set the rendered height

        Args: value: new rendered height
        """
        self._rendered_height = value

    @property
    def parent(self):
        """
        The parent of the widget. If None the widget
        is the top most widget usually a page Widget.
        """
        return self._parent

    @parent.setter
    def parent(self, widget):
        """
        Set the parent widget

        Args:
            value: the parent widget

        Returns:
            None
        """
        self._parent = widget

    @property
    def prev_widget(self):
        """
        The previous sibling widget
        """
        return self._parent.get_prev_sibling(self)

    @property
    def next_widget(self):
        """
        The next sibling widget
        """
        return self._parent.get_next_sibling(self)

    def get_prev_sibling(self, widget):
        """
        Calculate the previous sibling widget for a given widget

        Args:
            widget: The widget

        Returns:
            The previous sibling
        """
        widget_idx = self.content.index(widget)
        if widget_idx == 0:
            return self.parent
        return self.content[widget_idx - 1]

    def get_next_sibling(self, widget):
        """
        Calculate the next sibling widget for a given widget

        Args:
            widget: The widget

        Returns:
            The next sibling
        """
        widget_idx = self.content.index(widget)
        if widget_idx == len(self.content) - 1:
            return self.parent
        return self.content[widget_idx + 1]

    @property
    def length(self):
        """
        Return the length of the content. If the content is a string
        then the length of the string is returned.
        If the content is a list
        the number of elements is returned.
        """
        return len(self.content)

    @property
    def controller(self):
        """
        The controller adapter for the widget.
        This is in fact a caching for the controller adapter for performance.
        """
        return self._controller

    @property
    def has_focus(self):
        """
        Returns if the widget is currently focussed
        """
        gui = getUtility(IGUI)
        return gui.focus == self

    @classmethod
    def set_as_focus(self, widget):
        """
        Set myself as the focussed object
        """
        gui = getUtility(IGUI)
        gui.focus = widget
        if widget is not None and self.render_on_focus_change:
            widget.render()

    def render(self):
        """
        Render the widget on all displays
        """
        gui = getUtility(IGUI)
        for display in gui.displays:
            renderer = getMultiAdapter((self, display), IRenderer)
            if renderer:
                renderer.render()

    def clear(self):
        """
        Render the widget on all displays
        """
        gui = getUtility(IGUI)
        for display in gui.displays:
            renderer = getMultiAdapter((self, display), IRenderer)
            if renderer:
                renderer.clear()

    def handle_new_content(self, value):
        """
        Deal with new content.

        Args:
            value: THe new content
        """
        self._content = value
        # if render on contetn change is activated ..
        if self.render_on_content_change:
            #  .. render the widget to reflect the change
            self.render()

    def init(self):
        """
        Initialize the widget
        """
        pass

    def aquire_focus(self):
        """We got the focus"""
        if self.render_on_focus_change:
            self.render()

    def release_focus(self):
        """We lost the focus"""
        if self.render_on_focus_change:
            self.render()
