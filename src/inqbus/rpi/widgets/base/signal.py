

class Signal(object):
    """
    Representation of Signals.
    """

    def __str__(self):
        """
        The signal represents it self by its class name
        Returns:
        """
        return self.__class__.__name__
