class Event(object):

    def __str__(self):
        return self.__class__.__name__


class EventRegistry(object):
    def __init__(self):
        self.events = {}

    def register(self, event, callback):
        if event in self.events:
            self.events[event].append(callback)
        else:
            self.events[event] = [callback]

    def emit(self, event, **value):
        if event in self.events:
            for callback in self.events[event]:
                callback(**value)


event_registry = EventRegistry()
