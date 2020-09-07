.. inqbus.rpi.widgets documentation master file, created by
   sphinx-quickstart on Thu Sep  3 20:52:30 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to inqbus.rpi.widgets's documentation!
==============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


:doc:`background`

inqbus.rpi.widgets (IRW) is a basic framework for extensible GUI systems for the raspberryPi or other systems with small displays.
But there are no limits to extend or shape IRW.

IRW has the some neat features:

    * It is quite extensible due to its :doc:`component_design`.

    .. figure:: ./diagram_input.png
        :width: 800px
        :align: center
        :alt: alternate text
        :figclass: align-center

    .. figure:: ./diagram_output.png
        :width: 800px
        :align: center
        :alt: alternate text
        :figclass: align-center

    * Native support of a wide range of character displays

        IRW suports all the displays RPLCD can access (Hitachi mostly)

        And can easily be extended to support any display by implementing just two member functions::

            @implementer(IDisplay)
            class MyDisplay(Display):

            def set_cursor_pos(x, y)
                ...

            def write(string)
                ...

    * Character display emulation

        IRW has support for display emulation as
            * Curses
            * Console (e.g. for logging/debuggin of display changes)

        this enables you to develop your application on a desktop and then deploy it on the raspberry for debugging.

        .. note::

            This is not a true emulation of the Hitachi! It is just a framebuffer emulation.

    * Support of multiple displays in parallel

        You can write in parallel to all displays attached independed of their type

    * Support of multiple input devices in parallel

        You can attach any number of input devices.
        Blocking as well as non blocking input devices are supported.

        A non-blocking input device can coded simply as::

            @implementer(IInput)
            class MyInput(Input):

                def someone_has_clicked(self):
                    gui = getUtility(IGUI)
                    self.gui.dispatch(InputClick)

        For a blocking input device just change two lines::

            @implementer(IBlockingInput)
            class MyInput(BlockingInput):







:doc:`quickstart`
:doc:`introduction`
:doc:`component_design`



Indices and tables
==================

* :ref:`genindex`
* :doc:`apidoc/modules`
* :ref:`search`
