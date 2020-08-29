from inqbus.rpi.widgets.button import Button
from inqbus.rpi.widgets.line import Line
from inqbus.rpi.widgets.tests.base import TestBase


import inqbus.rpi.widgets.base.controller
import inqbus.rpi.widgets.gui


class TestButton(TestBase):

    def test_button(self, x=0, y=0):

        button = Button(x,y)
        button.content = 'huhu'

        self.widget_test(button)

        out_line = x * ' ' + '>' + button.content + '<' + ' ' * (self.display.width - len(button.content) - x -1)
        expected_result = out_line[:self.display.width ]

        assert self.display.frame_buffer[y] == expected_result


    def test_long_button_clipping(self, x=0, y=0):


        button = Button(x,y)
        button.content = 'huhu'

        self.widget_test(button)

        out_line = x * ' ' + '>' + button.content + '<' + ' ' * (self.display.width - len(button.content) - x -1)
        expected_result = out_line[:self.display.width ]

        assert self.display.frame_buffer[y] == expected_result


    def test_position(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.display.clear()
                self.test_button(x,y)

        for x in range(self.display.width):
            for y in range(self.display.height):
                self.display.clear()
                self.test_long_button_clipping(x,y)
