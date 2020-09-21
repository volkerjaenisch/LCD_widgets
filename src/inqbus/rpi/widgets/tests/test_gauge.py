from inqbus.rpi.widgets.gauge import Gauge
from inqbus.rpi.widgets.tests.base import TestBase


class TestGauge(TestBase):

    def gauge(self, widget):

        self.widget_set_as_layout(widget)

        expected_result = '→test:13.450°       '

        assert self.display.frame_buffer[0] == expected_result

    def test_gauge(self, x=0, y=0):

        widget = Gauge(
                'test',
                pos_x=x,
                pos_y=y,
                initial_value=13.45,
                increment=11.1,
                unit='°',
                format='3.3f',
        )
        self.gauge(widget)
