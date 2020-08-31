from inqbus.rpi.widgets.line import Line
from inqbus.rpi.widgets.lines import Lines
from inqbus.rpi.widgets.tests.base import TestBase


import inqbus.rpi.widgets.base.controller
import inqbus.rpi.widgets.gui
from inqbus.rpi.widgets.text import Text


class TestText(TestBase):

    def text(self, content_in, x=0, y=0):

        widget = Text(x,y)
        widget.content = content_in

        self.widget_test(widget)

        content = widget.content
        expected_result = []

        width = self.display.width - x
        start_pos = 0

        while True:
            rest_len = len(content[start_pos:])
            if width > rest_len:
                out_line = x * ' ' + content[start_pos:] + ' ' * (self.display.width - rest_len - x)
                expected_result.append(out_line)
                break
            else:
                out_line = x * ' ' + content[start_pos:start_pos + width]
                expected_result.append(out_line)
                start_pos += width

        pos_y = y
        for line in expected_result:
            assert self.display.frame_buffer[pos_y] == line
            pos_y += 1


    def test_text(self, x=0, y=0):

        self.text(15*'abcd')


    # def test_position(self):
    #     for x in range(self.display.width):
    #         for y in range(self.display.height):
    #             self.display.clear()
    #             self.test_lines_single(x,y)
    #             self.test_long_lines_single_clipping(x,y)
    #             self.test_lines_multi(x,y)
    #             self.test_long_lines_multi_clipping(x,y)
