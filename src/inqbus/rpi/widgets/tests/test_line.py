from inqbus.rpi.widgets.line import Line
from inqbus.rpi.widgets.tests.base import LONG_LINE, SHORT_LINE, TestBase


class TestLine(TestBase):

    def test_line(self, x=0, y=0):

        line = Line(x,y)
        line.content = SHORT_LINE

        self.widget_test(line)

        out_line = x * ' ' + line.content + ' ' * (self.display.width - len(line.content) - x)
        expected_result = out_line[:self.display.width ]

        assert self.display.frame_buffer[y] == expected_result


    def test_long_line_clipping(self, x=0, y=0):

        line = Line(x,y)
        line.content = LONG_LINE

        self.widget_test(line)

        out_line = x * ' ' + line.content + ' ' * (self.display.width - len(line.content) - x)
        expected_result = out_line[:self.display.width ]

        assert self.display.frame_buffer[y] == expected_result


    def test_position(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.display.clear()
                self.test_line(x,y)
                self.test_long_line_clipping(x,y)
