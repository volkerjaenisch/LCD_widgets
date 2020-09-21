from inqbus.rpi.widgets.gauge_target import GaugeTarget
from inqbus.rpi.widgets.tests.base import TestBase


class TestGaugeTarget(TestBase):

    def gauge(self, widget, x=0, y=0):

        self.widget_set_as_layout(widget)

        expected_result = '→test:13.450<23.710°'

        assert self.display.frame_buffer[0] == expected_result

    def test_gauge(self, x=0, y=0):

        widget = GaugeTarget(
                'test',
                pos_x=x,
                pos_y=y,
                initial_reading_value=13.45,
                initial_value=23.71,
                increment=11.1,
                unit='°',
                format='3.3f',
        )
        self.gauge(widget, x=x, y=y)
