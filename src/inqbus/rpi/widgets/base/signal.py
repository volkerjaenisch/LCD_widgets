

class Signal(object):
    """
    Representation of Signals.
    """

    def __str__(self):
        """
        The signal represents it self by its class name
        :return:
        """
        return self.__class__.__name__
