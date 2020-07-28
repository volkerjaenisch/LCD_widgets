a = input('eine Zahl: ')

from base.display import BaseDisplay

disp = BaseDisplay()

disp.write('huhu1')

disp.cursor_pos(1,0)

disp.write('huhu2')

disp.cursor_pos(1,3)

disp.write('Eulefuchsschwanzfurz')


disp.display()

