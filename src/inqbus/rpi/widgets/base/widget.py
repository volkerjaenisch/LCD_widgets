from inqbus.rpi.widgets.base.signals import SIGNAL_UP, SIGNAL_DOWN, SIGNAL_CLICK
from inqbus.rpi.widgets.log import logging


class Widget(object):
    _content = ''
    display = None
    autorender = True
    _selector = None

    def __init__(self, position, **kwargs):
        self.position = position
        if 'autorender' in kwargs:
            self.autorender = kwargs['autorender']

    @property
    def selectable(self):
        return self._selector is not None

    @selectable.setter
    def selectable(self, value):
        if value:
            self._selector = Selector(self, self.content)
        else:
            self._selector = None

    @property
    def selector(self):
        return self._selector

    def notify(self, signal):
        logging.debug('Signal received: ' + signal)
        logging.debug('Displatching signal :' + signal)
        if self.selectable:
            logging.debug('Displatching signal to selectable ' + signal)
            return self.selector.notify(signal)
        else:
            logging.debug('No one to dispatch to ' + signal)

    def render(self):
        pass

    def handle_new_content(self, value):
        self._content = value
        if self.autorender:
            self.render()
        if self.selector:
            self.selector.select_on = self.content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self.handle_new_content(value)


class Selector(object):
    _selected_idx = None
    _select_on = None
    _parent = None

    def __init__(self, parent, select_on, selected_idx=0):
        self.parent = parent
        self.select_on = select_on
        self.selected_idx = selected_idx
        self._signals = {
            SIGNAL_UP: self.on_up,
            SIGNAL_DOWN: self.on_down,
            SIGNAL_CLICK: self.on_click,
        }

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def select_on(self):
        return self._select_on

    @select_on.setter
    def select_on(self, value):
        self._select_on = value

    @property
    def selected_idx(self):
        return self._selected_idx

    @selected_idx.setter
    def selected_idx(self, value):
        self._selected_idx = value
        if self.parent and self.parent.autorender:
            self.parent.render()

    def active_item(self):
        return self.select_on[self.selected_idx]

    def on_click(self):
        return True

    def on_down(self):
        logging.debug(self.__class__.__name__ + ' selector on Down')
        #        import pdb; pdb.set_trace()

        if self.selected_idx < len(self.select_on) - 1:
            self.selected_idx += 1
            return True
        else:
            return False

    def on_up(self):
        logging.debug(self.__class__.__name__ + ' selector on Up')
        #        import pdb; pdb.set_trace()
        if self.selected_idx > 0:
            self.selected_idx -= 1
            return True
        else:
            return False

    def notify(self, signal):
        return self._signals[signal]()
