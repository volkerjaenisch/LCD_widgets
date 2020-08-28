from inqbus.rpi.widgets.line import Line
from inqbus.rpi.widgets.tests.base import TestBase


import inqbus.rpi.widgets.base.controller
import inqbus.rpi.widgets.gui


class TestLine(TestBase):

    def test_line(self):

        line = Line()
        line.content = 'huhu'

        self.widget_test(line)

        expected_result = line.content + ' ' * (self.display.width - len(line.content))

        assert self.display.frame_buffer[0] == expected_result

