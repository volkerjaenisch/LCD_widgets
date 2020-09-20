from inqbus.rpi.widgets.button import Button
from inqbus.rpi.widgets.config_default import FUCTION_CHARS_CURSES
from inqbus.rpi.widgets.tests.base import LONG_LINE, SHORT_BUTTON, TestBase


class TestButton(TestBase):

    def test_button(self, x=0, y=0):

        button = Button(pos_x=x, pos_y=y)
        button.content = SHORT_BUTTON

        self.widget_set_as_layout(button)
        before = ' ' * x
        after = ' ' * (self.display.width - len(button.content) - x - 1)
        out_line = before + FUCTION_CHARS_CURSES['FOCUS_LEFT'] + button.content + FUCTION_CHARS_CURSES['FOCUS_RIGHT'] + after
        expected_result = out_line[:self.display.width]

        assert self.display.frame_buffer[y] == expected_result

    def test_long_button_clipping(self, x=0, y=0):

        button = Button(pos_x=x, pos_y=y)
        button.content = LONG_LINE

        self.widget_set_as_layout(button)
        before = ' ' * x
        after = ' ' * (self.display.width - len(button.content) - x - 1)
        out_line = before + FUCTION_CHARS_CURSES['FOCUS_LEFT'] + button.content + FUCTION_CHARS_CURSES['FOCUS_RIGHT'] + after
        expected_result = out_line[:self.display.width]

        assert self.display.frame_buffer[y] == expected_result

    def test_position(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.display.clear()
                self.test_button(x=x, y=y)

        for x in range(self.display.width):
            for y in range(self.display.height):
                self.display.clear()
                self.test_long_button_clipping(x=x, y=y)
