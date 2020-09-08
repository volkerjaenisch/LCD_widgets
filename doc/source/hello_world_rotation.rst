Moving Hello World
==================


Text widget with label "Hello world" moves.

.. code-block:: python
    :linenos:

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

    display = DisplayCurses()

    gui = getUtility(IGUI)

    gui.add_display(display)
    gui.set_layout(text)

    gui.init()
    gui.run(blocking=False)

    while True:
        sleep(1)
        text.clear()
        text.pos_y = (text.pos_y + 1) % 4
        text.render()

    gui.done()


This should produce::
    .. figure:: ./hello_moving.gif
        :width: 800px
        :align: center
        :alt: alternate text
        :figclass: align-center



in your console.

.. note::

    If you are using PyCharm please check "Emulate terminal in output console" in your runtime configuration.


"Oh my god! So much boiler plate!" I hear you say.

Yes, for simply print out "hello world" this is much code.
But IRW is no display driver it is a GUI framework and any framework needs configuration.

Let's explain the code line by line to get familiar with it.

Lines 1-4 imports

    the CursesDisplay component,

    the gui Interface,

    the Text widget and

    the ZCA function getUtility.

In ZCA most of the operations with components are done using their associated interfaces - think "names".

Lines 6-9 Import the Components you like to use. IRW is extremely modular - you have to specify each component you like to use explicitly.

.. note::

    This is good python style. On the other hand it saves a lot of memory if you like to run your code on an architecture smaller than a raspberryPi.

Lines 11-12 Instantiate a Text-Widget and give it some content. IRW does not abuse the __init__ constructor.
Setting and changing properties on a widget has to be explicit, by a property call.

Line 14: Create a Curses Display instance. By default a display is 4 lines x 20 characters.

Line 16: To access the GUI component one ask the ZCA via its Interface (IGUI). This procedure
decouples the code since you no longer have to have a pointer to your top-level Object in any instance you are using.

Line 18: Add the display to the GUI

Line 19: Add the layout to the GUI

Line 21: Initialize the GUI. This initializes all the input and output devices at the hardware level.

Line 22: Run the GUI. The GUI main-loop is started which does the signal dispatching.
    The GUI is run in non blocking mode so we can add our own commands

Line 24-28:

    some delay

    clear(erase) the widget from the display

    give the widget a new position (circulate per modulo operation)

    render the widget at the new position




