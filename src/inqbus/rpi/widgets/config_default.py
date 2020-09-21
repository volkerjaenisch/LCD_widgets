
FUNCTION_CHARS_LCD = {
    'FOCUS_LEFT': chr(126),  # right arrow
    'FOCUS_RIGHT': chr(127),  # right arrow
    'CELSIUS': chr(223),
}

FUCTION_CHARS_CURSES = {
    'FOCUS_LEFT': '→',  # right arrow
    'FOCUS_RIGHT': '←',  # right arrow
    'CELSIUS': '°',
}

CHARMAP_LCD = {
   '°': chr(223),
}

FROM = ''.join(CHARMAP_LCD.keys())
TO = ''.join(CHARMAP_LCD.values())

CHAR_TRANSLATION_LCD = str.maketrans(FROM, TO)
