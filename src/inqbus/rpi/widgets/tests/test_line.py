from inqbus.rpi.widgets.line import Line
from inqbus.rpi.widgets.tests.base import LONG_LINE, SHORT_LINE, TestBase


class TestLine(TestBase):

    def line_run(self, content, x=0, y=0):

        line = Line(pos_x=x, pos_y=y)
        line.content = content

        self.widget_set_as_layout(line)

        space_before = ' ' * x
        space_after = ' ' * (self.display.width - len(line.content) - x)
        out_line = space_before + line.content + space_after
        expected_result = out_line[:self.display.width]

        assert self.display.frame_buffer[y] == expected_result

    def test_position(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.display.clear()
                self.line_run(SHORT_LINE, x, y)
                self.line_run(LONG_LINE, x, y)
