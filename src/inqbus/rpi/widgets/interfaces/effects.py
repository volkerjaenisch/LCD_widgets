from zope.interface import Interface


class IBlinking(Interface):
    """
    Set a widget to do blinking
    """


class IScrollWrapper(Interface):
    """
    Wrapps a widget to modifiy its content to simulate scrolling
    """


class IScrolling(Interface):
    """
    Set a widget to do scrolling
    """
