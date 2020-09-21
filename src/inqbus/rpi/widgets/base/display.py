from threading import Lock
from time import sleep

from inqbus.rpi.widgets.base.device import Device
from inqbus.rpi.widgets.errors import OutOfDisplay
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class Display(Device):
    """
    The frame_buffer base class implements
    the access to the physical frame_buffer e.g. to
    * initialize the underlying hardware
    * catch out of bounds errors
    * give the Display a Lock for multithreading
    """

    # states if the frame_buffer is ready to accept requests.
    # Mainly to prevent writes to non initialized hardware.
    initialized = False

    def __init__(self,
                 height=4,
                 width=20,
                 autoupdate=True,
                 ):
        self.autoupdate = autoupdate
        self.height = height
        self.width = width
        self.pos_x = 0
        self.pos_y = 0
        # Threading.Lock isntance to serialize write operations
        # from different render threads
        self.lock = Lock()

    def clear(self):
        """
        Clear the display
        """
        pass

    def init(self):
        """
        Initialize the display
        """
        super(Display, self).init()

    def run(self):
        """
        Activate the display
        """
        pass

    def done(self):
        """
        Deactivate the display
        """
        pass

    def write_at_pos(self, x, y, content):
        """
        Write at the given display position the string in content.
        Make use of a lock to prevent that concurrent threads are using the display driver at the same time.

        Args:
            x: Horizontal display postiton
            y: Vertical display postiton
            content: The string to be written

        Returns:
            None
        """

        with self.lock:
            try:
                self.set_cursor_pos(x, y)
                self.write(content)
            except OutOfDisplay:
                return

    def set_cursor_pos(self, x, y):
        """
        Set the cursor position.

        Args:
            x: Horizontal position
            y: Vertical position

        Returns:
            None
        """
        if not y < self.height:
            raise OutOfDisplay
        if not x < self.width:
            raise OutOfDisplay
        self.pos_x, self.pos_y = (x, y)

    def write(self, content):
        pass
