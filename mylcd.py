from RPLCD.i2c import CharLCD


class Widget(object):
    
    _content = ''
    display = None
    autorender = True
    
    def __init__(self, position, **kwargs):
        self.position = position
        if 'autorender' in kwargs:
            self.autorender = kwargs['autorender']
        
    def signal(self, signal, value=None):
        print('Signal received', signal)
        getattr(self, signal)()
        
    def render(self):
        pass

    def handle_new_content(self, value):
        self._content = value
        if self.autorender:
            self.render()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self.handle_new_content(value)

        
class Selectable(object):
    
    _selected_idx = None
    _parent = None

    def __init__(self, selected_idx=0):
        self.selected_idx = selected_idx
        self._signals = {
            'up', self.on_up,
            'down', self.on_down,
            'click', self.on_click,
            }
        
    @property
    def parent(self):
        return self._parent
        
    @parent.setter
    def parent(self, value):
        self._parent = value
    
    @property
    def selected_idx(self):
        return self._selected_idx
        
    @selected_idx.setter
    def selected_idx(self, value):
        self._selected_idx = value
        if self.parent and self.parent.autorender:
            self.parent.render()

    def on_click(self):
        pass

    def on_down(self):
        if self.selected_idx < self.line_count:
            self.selected_idx += 1
        else:
            self.parent.down()
        
    def on_up(self):
        if self.selected_idx > 1 :
            self.selected_idx -= 1
        else:
            self.parent.up()
            
    def on_signal(self, signal):
        self._signals[signal]()

        
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

    
    def __init__(self, position, line_count, selectable):
        super(Lines, self).__init__(position)
        self.line_count = line_count
        self.selectable = selectable
        
    def handle_selectable(self, value):
        self._selectable = value
        self._selectable.parent = self
        
    @property
    def selectable(self):
        return self._selectable

    @selectable.setter
    def selectable(self, value):
        self.handle_selectable(value)
        
    def handle_new_content(self, value):
        super(Select, self).handle_new_content(value)
        
    def render(self):
        y_pos, x_pos = self.position
        for idx, line in enumerate(self.content[0:self.line_count]):
            self.display.cursor_pos(y_pos, x_pos)
            if  idx == self.selectable.selected_idx:
                self.display.write('>' + line)
            else:
                self.display.write(' ' + line)
                
            y_pos += 1

            
class Page(Widget):
    widgets = []
    
    def __init__(self, display, parent=None, selectable=None):
        self.display = display
        self.parent = parent
        self.selectable = selectable
            
    def add_widget(self, widget):
        widget.display = self.display
        widget.parent = self
        self.widgets.append(widget)

    def active_widget(self):
        return self.widgets[0]
        
    def render(self):
        for widget in self.widgets:
            widget.render()

    def signal(self, signal, value=None):
        print('Signal received', signal)
        getattr(self.active_widget(), signal)()
        
            
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
        self.active_page.signal('up')

    def down(self):
        print('sended signal down')
        self.active_page.signal('down')

    def click(self):
        print('sended Signal click')
        self.active_page.signal('click')
    
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
body = Select((1,0), 3, Selectable())

start_page.add_widget(header)
start_page.add_widget(body)

header.content = 'Hallo'
body.content = ['Volker', 'Du', 'Aas']

header.content = 'Huhu'

controller.active_page = start_page
controller.register_input(InputRotary)

controller.loop()
