from zope.interface import Interface, Attribute


class IWidget(Interface):

    content = Attribute('Content of widget')
    pos_x = Attribute('X position of widget')
    pos_y = Attribute('Y position of widget')
    width = Attribute('Width of widget')
    height = Attribute('Height of widget')
    parent = Attribute('Parent widget')
    content_length = Attribute(
            'Length of the content e.g. number of select item')
    prev_widget = Attribute('Previous sibling widget')
    next_widget = Attribute('Next sibling widget')
    controller = Attribute('Controller for the widget')
    has_focus = Attribute('is the widget focussed')

    def get_prev_sibling(self, widget):
        """Get from the parent widget the previous sibling"""

    def get_next_sibling(self, widget):
        """Get from the parent widget the following sibling"""

    def render(self, pos_x=None, pos_y=None):
        """Render the widget"""

    def handle_new_content(self, value):
        """Handle the addition of new content"""

    def init(self):
        """Initialize"""
        pass

    def aquire_focus(self):
        """We got the focus"""

    def release_focus(self):
        """We lost the focus"""


class ILineWidget(IWidget):
    pass


class ITextWidget(IWidget):
    pass


class IButtonWidget(ILineWidget):
    pass


class ICheckboxWidget(IButtonWidget):
    pass


class IGaugeWidget(ILineWidget):
    pass


class IGaugeTargetWidget(ILineWidget):
    pass



class ILinesWidget(IWidget):
    pass


class ISelectWidget(IWidget):
    pass


class IPageWidget(IWidget):
    pass
