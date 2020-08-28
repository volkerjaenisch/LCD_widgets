from threading import Lock

from inqbus.rpi.widgets.base.device import Device
from inqbus.rpi.widgets.errors import OutOfDisplay
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class Display(Device):
    """
    The frame_buffer base class implements the access to the physical frame_buffer e.g. to
    * initialize the underlying hardware
    * catch out of bounds errors
    * give the Display a Lock for multithreading
    """
    # states if the frame_buffer is ready to accept requests. Mainly to prevent writes to non initialized hardware.
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
        # Threading.Lock isntance to serialize write operations from different render threads
        self.lock = Lock()

    def init(self):
        super(Display, self).init()

    def run(self):
        pass

    def done(self):
        pass

    def write_at_pos(self, x, y, content):
        # Use the threading Lock
        with self.lock:
            try:
                self.set_cursor_pos(x, y)
                self.write(content)
            except OutOfDisplay:
                return

    def set_cursor_pos(self, x, y):
        if not y < self.height :
            raise OutOfDisplay
        if not x < self.width :
            raise OutOfDisplay
        self.pos_x, self.pos_y = (x, y)

    def write(self, content):
        pass
