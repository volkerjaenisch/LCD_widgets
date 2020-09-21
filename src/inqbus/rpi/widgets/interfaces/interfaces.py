from zope.interface import Interface, Attribute


class IRenderer(Interface):
    """
    Each Widget has its own renderers.
    Each Renderer is a multi adapter for a widget and a frame_buffer type.
    """

    def render(self):
        pass


class IDevice(Interface):
    """
    Base interface for a hardware device may it be input our output device
    """

    def init(self):
        """Initialize (boot, interface with) the device"""
        pass

    def run(self):
        """Send the Device a start action"""
        pass

    def done(self):
        """Dispose of the Device"""
        pass


class IWidgetController(Interface):
    """
    The Widget controller deals with actions changing state of the widget.
    E.g. the widget controller of a select takes input signals like up/down and
    reflects them onto the internal state of the widget.

    There are three actions currently implemented:
        click,
        up,
        down
    """

    def on_click(self, signal):
        """Handler for click"""

    def on_down(self, signal):
        """Handler for down"""

    def on_up(self, signal):
        """Handler for up"""

    def notify(self, signal):
        """Signal dispatcher"""


class INotify(Interface):
    """
    Event abstraction. Currently Events are not more than function calls.
    """

    def notify(self, signal):
        """dispatch an instance od a signal"""


class IMoveFocus(Interface):
    """
    Handles focus moves on signals
    """

    def on_up(self, signal):
        """
        Focus moves up
        """

    def on_down(self, signal):
        """
        Focus moves down
        """


class IGUI(Interface):
    focus = Attribute("""The single focussed widget""")
