from RPLCD.i2c import CharLCD

SIGNAL_UP = 'up'
SIGNAL_DOWN = 'down'
SIGNAL_CLICK = 'click'


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
            self._selector = Selector( self, self.content )
        else :
            self._selector = None

    @property
    def selector(self):
        return self._selector
        
    def notify(self, signal):
        print('Signal received', signal)
        print('Displatching signal', signal)
        if self.selectable :
            print('Displatching signal to selectable', signal)
            return self.selector.notify( signal )
        else:
            print('No one to dispatch to', signal)
            
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
            SIGNAL_UP : self.on_up,
            SIGNAL_DOWN : self.on_down,
            SIGNAL_CLICK : self.on_click,
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
        print(self.__class__.__name__, 'selector on Down')
#        import pdb; pdb.set_trace()
        
        if self.selected_idx < len(self.select_on) - 1:
            self.selected_idx += 1
            return True
        else:
            return False
        
    def on_up(self):
        print(self.__class__.__name__, 'selector on Up')
#        import pdb; pdb.set_trace()
        if self.selected_idx > 0 :
            self.selected_idx -= 1
            return True
        else:
            return False
            
    def notify(self, signal):
        return self._signals[signal]()

    
        
class Line(Widget):
    
    def render(self):
        self.display.cursor_pos(*self.position)
        
        out_line = self.content
        out_line +=  (self.display.chars_per_line - len(self.content)) * ' '
        self.display.write(out_line)

    def clear_line(self, line_number=None):
        if line_number:
            self.lcd.cursor_pos = (line_number, 0)
        self.lcd.write_string(' ' * self.chars_per_line)

        
class Lines(Line):
    _content = []

    def __init__(self, position, line_count):
        super(Lines, self).__init__(position)
        self.line_count = line_count
        
                
    def render(self):
        y_pos, x_pos = self.position
        for line in self.content[0:self.line_count]:
            self.display.cursor_pos(y_pos, x_pos)
            y_pos += 1
            self.display.write(line)
        

class Select(Lines):
    _content = []
    _selectable = None

    
    def __init__(self, position, line_count):
        super(Lines, self).__init__(position)
        self.line_count = line_count
        self.selectable = True
        
        
    def handle_selectable(self, value):
        self.selectable = value
                 
    def handle_new_content(self, value):
        super(Select, self).handle_new_content(value)
        
    def render(self):
        y_pos, x_pos = self.position
        for idx, line in enumerate(self.content[0:self.line_count]):
            self.display.cursor_pos(y_pos, x_pos)
            if  idx == self.selector.selected_idx:
                self.display.write('>' + line)
            else:
                self.display.write(' ' + line)
                
            y_pos += 1

            
class Page(Widget):
    widgets = []
    selectable_widgets = []
    
    def __init__(self, display, parent=None):
        self.display = display
        self.parent = parent
        self._selector = Selector( self, self.selectable_widgets )    
        
    def add_widget(self, widget):
        widget.display = self.display
        widget.parent = self
        self.widgets.append(widget)
        self.check_mark_selectable(widget)
        
    def check_mark_selectable(self, widget):
        if widget.selectable :
            self.selectable_widgets.append(widget)

    def set_selectable( self, widget ):
        if widget in self.selectable_widgets:
            return
        else: 
            self.selectable_widgets = []
            for widget in self.widgets:
                self.check_mark_selectable( widget)
            
    def active_widget(self):
        if not self.selectable_widgets:
            return None
        return self.selectable_widgets[0]
        
    def render(self):
        for widget in self.widgets:
            widget.render()

    def handle_signal(self, signal):
        self.selector.notify( signal )
            
    def notify(self, signal, value=None):
        print('Page received Signal:', signal)
        target = self.active_widget()
        if not target : 
            return
        res = target.notify(signal)
        if res :
            return
        else:
            self.handle_signal(signal)
            
            
        
            
class Display(object):
    
    def __init__(self, line_count=4, chars_per_line=20):
        self.line_count = line_count
        self.chars_per_line = chars_per_line
        
        self.init_display()
        
    def init_display(self):
        
        self.lcd = CharLCD('PCF8574', 0x27, backlight_enabled=True)
#        self.lcd = CharLCD('MCP23017', 0x20, backlight_enabled=True, expander_params={'gpio_bank': 'B'})
        self.lcd.clear()
        self.lcd.write_string('huhu')
        
    def cursor_pos(self, y, x):
        self.lcd.cursor_pos = (y, x)

    def write(self, line):
        self.lcd.write_string(line)
                      


        
        
class Controller(object):
    
    _active_page = None
    
    @property
    def active_page(self):
        return self._active_page
        
    @active_page.setter
    def active_page(self, value):
        self._active_page = value
        self._active_page.render()
    
    def up(self):
        print('sended signal up')
        self.active_page.notify(SIGNAL_UP)

    def down(self):
        print('sended signal down')
        self.active_page.notify(SIGNAL_DOWN)

    def click(self):
        print('sended Signal click')
        self.active_page.notify(SIGNAL_CLICK)
    
    def register_input(self, input_cls):
        self.input = input_cls(
            self.up,
            self.down,
            self.click,
            )

    def loop(self):
        while True:
            sleep(1)
        
        
class Input(object):
    up_handler = None
    down_handler = None
    click_handler = None


from pigpio_encoder import Rotary
from time import sleep


class InputRotary(Input):

    rotary = None
    counter = None
    
    def __init__(self, up_handler, down_handler, click_handler):
        self.up_handler = up_handler
        self.down_handler = down_handler
        self.click_handler = click_handler
        self.rotary = Rotary(clk=17, dt=22, sw=27)
        self.rotary.setup_rotary(rotary_callback=self.rotary_callback)
        self.rotary.setup_switch(sw_short_callback=self.click_callback)
        
    
    def rotary_callback(self, counter):
        print('Rotation', counter)
        if not self.counter:
            self.counter = counter
            return
        if counter > self.counter:
            self.counter = counter
            self.up_handler()
        elif counter < self.counter:
            self.counter = counter
            self.down_handler()
    
    def click_callback(self):
        print('Click!')
        self.click_handler()
    
            
display = Display()
controller = Controller()

start_page = Page(display)

header = Line((0, 0))
body = Select((1,0), 3 )

start_page.add_widget(header)
start_page.add_widget(body)

header.content = 'Hallo'
body.content = ['Volker', 'Du', 'Aas']

header.content = 'Huhu'

controller.active_page = start_page
controller.register_input(InputRotary)

controller.loop()
