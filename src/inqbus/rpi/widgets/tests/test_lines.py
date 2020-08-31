from inqbus.rpi.widgets.line import Line
from inqbus.rpi.widgets.lines import Lines
from inqbus.rpi.widgets.tests.base import TestBase


import inqbus.rpi.widgets.base.controller
import inqbus.rpi.widgets.gui


class TestLines(TestBase):

    def lines_single(self, content_in, x=0, y=0):

        lines = Lines(x,y)
        lines.content = content_in

        self.widget_test(lines)

        content = lines.content[0].content
        out_line = x * ' ' + content + ' ' * (self.display.width - len(content) - x)
        expected_result = out_line[:self.display.width ]

        assert self.display.frame_buffer[y] == expected_result


    def lines_multi(self, content_in, x=0, y=0):

        lines = Lines(x,y)
        lines.content = content_in

        self.widget_test(lines)
        expected_result = []
        pos_y = y
        for line in lines.content:
            if pos_y > self.display.height - 1:
                break
            content = line.content
            out_line = x * ' ' + content + ' ' * (self.display.width - len(content) - x)
            expected_result.append(out_line[:self.display.width ])

        pos_y = y
        for line in expected_result:
            if pos_y > self.display.height - 1:
                break
            assert self.display.frame_buffer[pos_y] == line
            pos_y += 1

    def test_lines_single(self, x=0, y=0):

        self.lines_single(['abcd'])


    def test_long_lines_single_clipping(self, x=0, y=0):

        self.lines_single([15 * 'abcd'])

    def test_lines_multi(self, x=0, y=0):

        self.lines_multi(['abcd', 'volker', 'hugo', 'otto', 'gerald'])


    def test_long_lines_multi_clipping(self, x=0, y=0):

        self.lines_multi([10*'abcd', 11*'volker', 12*'hugo', 13*'otto', 14*'gerald'])

    def test_position(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.display.clear()
                self.test_lines_single(x,y)
                self.display.clear()
                self.test_long_lines_single_clipping(x,y)
                self.display.clear()
                self.test_lines_multi(x,y)
                self.display.clear()
                self.test_long_lines_multi_clipping(x,y)
