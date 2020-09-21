from threading import Lock

from bitarray._bitarray import bitarray
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
        # Session for render events. Features a cleaning_mask of bits
        self._session_holder = None
        self.setup_cleaning_buffer()

    def setup_cleaning_buffer(self):
        self.cleaning_mask = []
        for y in range(self.height):
            cleaning_mask = bitarray(self.width)
            cleaning_mask.setall(False)
            self.cleaning_mask.append(cleaning_mask)

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
        Make use of a lock to prevent that concurrent threads
        are using the display driver at the same time.

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
                self.write_to_cleaning_mask(x, y, content)
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

    def open_session(self, renderer):
        if self._session_holder is None:
            self._session_holder = renderer

    def commit_session(self, renderer):
        if renderer == self._session_holder:
            self.flush_cleaning_mask()

    def write_to_cleaning_mask(self, x, y, content):
        self.cleaning_mask[y][x:x + len(content)] = False

    def erase_from_cleaning_mask(self, x, y, content_length):
        if y < self.height:
            self.cleaning_mask[y][x:x + content_length] = True

    def flush_cleaning_mask(self):
        for y, cleaning_mask in enumerate(self.cleaning_mask):
            start = 0
            while True:
                try:
                    true_start = cleaning_mask.index(True, start)
                except ValueError:
                    break
                try:
                    true_end = cleaning_mask.index(False, true_start)
                    self.write_at_pos(
                            true_start,
                            y,
                            ' ' * (true_end-true_start))
                except ValueError:
                    self.write_at_pos(
                            true_start,
                            y,
                            ' ' * (self.width-true_start)
                    )
                    break

        self.setup_cleaning_buffer()
        self._session_holder = None
