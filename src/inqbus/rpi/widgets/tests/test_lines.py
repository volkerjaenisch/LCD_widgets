from inqbus.rpi.widgets.lines import Lines
from inqbus.rpi.widgets.tests.base import TestBase


class TestLines(TestBase):

    def lines_single(self, content_in, x=0, y=0):

        lines = Lines(pos_x=x, pos_y=y)
        lines.content = content_in

        self.widget_set_as_layout(lines)

        content = lines.content[0].content
        space_before = ' ' * x
        space_after = ' ' * (self.display.width - len(content) - x)
        out_line = space_before + content + space_after
        expected_result = out_line[:self.display.width]

        assert self.display.frame_buffer[y] == expected_result

    def lines_multi(self, content_in, x=0, y=0):

        lines = Lines(pos_x=x, pos_y=y)
        lines.content = content_in

        self.widget_set_as_layout(lines)
        expected_result = []
        pos_y = y
        for line in lines.content:
            if pos_y > self.display.height - 1:
                break
            content = line.content
            space_before = ' ' * x
            space_after = ' ' * (self.display.width - len(content) - x)
            out_line = space_before + content + space_after
            expected_result.append(out_line[:self.display.width])

        pos_y = y
        for line in expected_result:
            if pos_y > self.display.height - 1:
                break
            assert self.display.frame_buffer[pos_y] == line
            pos_y += 1

    def test_lines_single(self, x=0, y=0):

        self.lines_single(['This is a short line'], x=x, y=y)

    def test_long_lines_single_clipping(self, x=0, y=0):

        self.lines_single([15 * 'abcd'], x=x, y=y)

    def test_lines_multi(self, x=0, y=0):

        content = [
            'abcd',
            'volker',
            'hugo',
            'otto',
            'gerald'
        ]
        self.lines_multi(content, x=x, y=y)

    def test_long_lines_multi_clipping(self, x=0, y=0):

        content = [
            10*'abcd',
            11*'volker',
            12*'hugo',
            13*'otto',
            14*'gerald'
        ]
        self.lines_multi(content, x=x, y=y)

    def test_position(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.display.clear()
                self.test_lines_single(x=x, y=y)
                self.display.clear()
                self.test_long_lines_single_clipping(x=x, y=y)
                self.display.clear()
                self.test_lines_multi(x=x, y=y)
                self.display.clear()
                self.test_long_lines_multi_clipping(x=x, y=y)
