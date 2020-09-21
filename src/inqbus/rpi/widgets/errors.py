
class SignalNotCatched(Exception):
    """Raised when a widget cannot process a signal.
    E.g. when a select gets a Signal up but it is already
    at the topmost position"""
    pass


class OutOfDisplay(Exception):
    """Raised when a write out of the bounds of the frame_buffer occurs"""
    pass
