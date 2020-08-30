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

        try :
            assert self.display.frame_buffer[y] == expected_result
        except:
            pass


    def lines_multi(self, content_in, x=0, y=0):

        lines = Lines(x,y)
        lines.content = content_in

        self.widget_test(lines)
        expected_result = []
        for line in lines.content:
            content = line.content
            out_line = x * ' ' + content + ' ' * (self.display.width - len(content) - x)
            expected_result.append(out_line[:self.display.width ])

        try :
            pos_y = y
            for line in expected_result:
                assert self.display.frame_buffer[pos_y] == line
                pos_y += 1
        except:
            pass


    def test_lines_single(self, x=0, y=0):

        self.lines_single(['abcd'])


    def test_long_lines_single_clipping(self, x=0, y=0):

        self.lines_single([15 * 'abcd'])

    def test_lines_multi(self, x=0, y=0):

        self.lines_multi(['abcd', 'volker', 'hugo'])


    def test_long_lines_multi_clipping(self, x=0, y=0):

        self.lines_multi([15*'abcd', 15*'volker', 15*'hugo'])


    def test_position(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.display.clear()
                self.test_lines_single(x,y)
                self.test_long_lines_single_clipping(x,y)
                self.test_lines_multi(x,y)
                self.test_long_lines_multi_clipping(x,y)
