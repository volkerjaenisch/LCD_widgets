import threading
from queue import Empty, Queue
from time import sleep

from inqbus.rpi.widgets.interfaces.input import IBlockingInput
from inqbus.rpi.widgets.interfaces.interfaces import IGUI, IMoveFocus, IWidgetController
from zope.component import getGlobalSiteManager
from zope.interface import implementer


@implementer(IGUI, IWidgetController)
class GUI(object):
    """
    The top most model instance.
    The GUI knows the registered displays and inputs as well as
    the widget tree (_layout).
    It manages the _focus state and holds the signal queue.
    """

    def __init__(self):
        # THe GUI knows the registered displays
        self._displays = []
        # and inputs
        self._inputs = []
        # as well as the tree of widgets
        self._layout = None
        # It manages the focused widget state
        self._focus = None
        # and holds the signal queue to dispatch Signals from the inputs
        self.signal_queue = Queue()

    def add_display(self, display):
        """
        Register a display device.

        Args:
            display:
                The display to register
        """
        self._displays.append(display)

    def add_input(self, input_dev):
        """
        Register an input_dev device.

        Args:
            input_dev:
                The input_dev to register
        """
        self._inputs.append(input_dev)

    def set_layout(self, layout):
        """
        Set the layout

        Args:
            layout: The layout to be set
        """
        self._layout = layout
        # Also set the focus to the topmost widget.
        self._focus = self._layout

    @property
    def focus(self):
        """
        The current focussed widget
        """
        return self._focus

    @focus.setter
    def focus(self, widget):
        """
        Set the current focus to the given widget

        Args:
            widget: The widget to set the focus upon
        """
        self._focus = widget

    def init(self):
        """
        Initialize the GUI
        """

        # Initialize the frame_buffer devices and start them
        for display in self._displays:
            display.init()
            display.run()

        for input_dev in self._inputs:
            # Initialize the input_dev devices and start them
            input_dev.init()
            # if an input_dev device is blocking
            # start it in a thread and connect it to the signal queue
            if IBlockingInput.providedBy(input_dev):
                thread = threading.Thread(
                        target=input_dev.run,
                        args=(self.signal_queue, )
                )
                thread.start()
            else:
                # .. else simply start the input_dev device
                input_dev.run()

    def run(self):
        """
        Run the GUI
        """
        # Initial Render
        self._layout.render()
        # Entering the signal processing loop
        self.signal_loop()

    def signal_loop(self):
        """
        The main signal loop for the thread of blocking input_dev devices
        """

        while True:
            # check the queue for new signal
            try:
                signal = self.signal_queue.get(block=False)
                # dispatch the signal
                self.dispatch(signal)
            # if the queue is empty just continue after some small wait
            except Empty:
                pass
            sleep(0.1)

    def dispatch(self, signal):
        """
        Top level signal dispatcher.
        Will be called from the signal queue
        as well as the nonblocking inputs directly.

        Args: signal: The signal to dispatch
        Returns:
            True if the signal could be dispatched, False if not
        """

        # dispatch the signal to the focussed widget's controller
        result = self.focus.controller.dispatch(signal)
        # If the focussed widget has consumed the signal ..
        if result:
            # .. return True for success to the caller
            return True
        else:
            # ..else do a MoveFocus Operation
            result = IMoveFocus(self)(signal)
            # and return its result
            return result

    @property
    def displays(self):
        """
        All registered displays
        """
        return self._displays

    def render(self):
        """
        Top level render function
        """
        # Render the widget tree
        self._layout.render()


gsm = getGlobalSiteManager()

# The main GUI instance
gui = GUI()
# is registered as a global utility
gsm.registerUtility(gui, IGUI)
