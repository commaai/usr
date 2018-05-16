class Color:
    black = '30'
    darkred = '31'
    darkgreen = '32'    
    brown = '33'
    darkblue = '34'
    purple = '35'
    teal = '36'
    lightgray = '37'
    darkgray = '30;01'
    red = '31;01'
    green = '32;01'
    yellow = '33;01'
    blue = '34;01'
    fuchsia = '35;01'
    turquoise = '36;01'
    white = '37;01'

    green_bg = '42'

    @classmethod
    def set(cls, color, string):
        try:
            color = getattr(cls, color)
        except AttributeError:
            pass
        return '\x1b[%sm%s\x1b[00m' % (color, string)

