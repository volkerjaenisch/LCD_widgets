from inqbus.rpi.widgets.tests.base import LONG_LINE, SHORT_LINE, TINY_LINE, TestBase
from inqbus.rpi.widgets.text import Text


class TestText(TestBase):

    def text(self, widget, x=0, y=0):


        self.widget_test(widget)

        content = widget.content
        expected_result = []

        if widget.width :
            width = widget.width
        else:
            width = self.display.width - x
        start_pos = 0

        while True:
            rest_len = len(content[start_pos:])
            if width > rest_len:
                out_line = x * ' ' + content[start_pos:] + ' ' * (self.display.width - rest_len - x)
                out_line = out_line[:self.display.width]
                expected_result.append(out_line)
                break
            else:
                out_line = x * ' ' + content[start_pos:start_pos + width] + ' ' * ( self.display.width - width - x)
                out_line = out_line[:self.display.width]
                expected_result.append(out_line)
                start_pos += width

        pos_y = y
        for line in expected_result[:self.display.height]:
            if pos_y > self.display.height - 1:
                break
            assert self.display.frame_buffer[pos_y] == line
            pos_y += 1


    def test_text(self, x=0, y=0):

        widget = Text(x,y)
        widget.content = TINY_LINE
        self.text(widget,x=x, y=y)

        widget = Text(x,y)
        widget.content = SHORT_LINE
        self.text(widget,x=x, y=y)

        widget.width = 5
        self.text(widget,x=x, y=y)

        widget.content = LONG_LINE
        self.text(widget,x=x, y=y)


    def test_position(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.test_text(x,y)
