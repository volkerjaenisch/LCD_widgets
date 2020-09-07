Introduction
============

RPLCD_widgets consists of a set of components to build an gui application with

    * different input devices (Rotary encoder, keyboard, etc.)
    * different simultaneuos output devices (LCD-Character Display, console/log-file, etc.)
    * a gui of linked pages with widgets

A minimal application needs a

    * a gui (the main loop and top level widget)
    * an output device
    * a widget to render

Hello world::

    from inqbus.rpi.widgets.display.curses import DisplayCurses
    from inqbus.rpi.widgets.interfaces.interfaces import IGUI
    from inqbus.rpi.widgets.text import Text
    from zope.component import getUtility

    # load the gui component
    import inqbus.rpi.widgets.gui # IMPORTANT!
    # load the base controller component
    import inqbus.rpi.widgets.base.controller # IMPORTANT!

    text = Text()
    text.content = 'Hello World'

    gui = getUtility(IGUI)
    display = DisplayCurses()

    gui.add_display(display)
    gui.set_layout(text)

    gui.init()
    gui.run(blocking=False)

