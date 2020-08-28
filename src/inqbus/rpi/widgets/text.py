from inqbus.rpi.widgets.base.widget import Widget
from inqbus.rpi.widgets.interfaces.widgets import ITextWidget
from zope.interface import implementer


@implementer(ITextWidget)
class Text(Widget):
    """
    Text Widget. Representing a single read only string of characters that is broken into lines to float into the given space.
    """
    def handle_new_content(self, value):
        assert isinstance(value, str)
        super(Text, self).handle_new_content(value)

