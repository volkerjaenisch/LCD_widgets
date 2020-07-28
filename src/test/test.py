from inqbus.rpi_widgets.widgets.base import Display

disp = Display()

disp.write('huhu1')

disp.cursor_pos(1,0)

disp.write('huhu2')

disp.cursor_pos(1,3)

disp.write('Eulefuchsschwanzfurz')

disp.show()

