from zope.interface import Interface, Attribute


class IGUI(Interface):
    pass


class IWidget(Interface):

    content = Attribute("""Content of widget""")
    pos_x = Attribute("""X position of widget""")
    pos_y = Attribute("""Y position of widget""")
    parent = Attribute("""X,Y position of widget""")

    def length(self):
        pass

    def init(self):
        pass


class ILineWidget(IWidget):
    pass


class ILinesWidget(IWidget):
    pass


class ISelectWidget(IWidget):
    pass


class IPageWidget(IWidget):
    pass


class IRenderer(Interface):

    def render(self):
        pass


class IDevice(Interface):

    def init(self):
        pass

    def run(self):
        pass

    def done(self):
        pass


class IDisplay(IDevice):

    def write_at_pos(self, x, y, content):
        pass


class IRPLCD(IDisplay):
    pass


class ICharLCD(IDisplay):
    pass


class ICurses(IDisplay):
    pass


class IInput(IDevice):
    pass


class IBlockingInput(IInput):
    queue = Attribute("""Sync-Queue to main thread""")

    def run(self, queue):
        pass


class IWidgetController(Interface):
    pass


class ILayout(Interface):

    focus = Attribute("""Focussed widget""")


class INotify(Interface):
    pass
