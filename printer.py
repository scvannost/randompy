from collections import OrderedDict

class colorprinter:
    """
A class to print in fun colors/styles with.
Methods:
    colors: returns the list of possible text colors in order
    backgrounds: returns the list of possible background colors in order
    reverse: uses print to make a white font on a black background
    print: extends the regular print function with fun add-ons; see print.__doc__
    _print: the original print function.
    """
    _colors = OrderedDict([ # a library of all the things
        ('BLACK' , '\033[30m'),
        ('DARKRED' , '\033[31m'),
        ('DARKGREEN' , '\033[32m'),
        ('ORANGE' , '\033[33m'),
        ('DARKBLUE' , '\033[34m'),
        ('PURPLE' , '\033[35m'),
        ('DARKCYAN' , '\033[36m'),
        ('LIGHTGREY' , '\033[37m'), ('LIGHTGRAY', '\033[37m'),
        
        ('DARKGREY' , '\033[90m'), ('DARKGRAY' , '\033[90m'),
        ('RED' , '\033[91m'),
        ('GREEN' , '\033[92m'),
        ('YELLOW' , '\033[93m'),
        ('BLUE' , '\033[94m'),
        ('MAGENTA' , '\033[95m'),
        ('CYAN' , '\033[96m'),
        ('GREY' , '\033[97m'), ('GRAY' , '\033[97m'),
        
        ('BOLD' , '\033[1m'),
        ('UNDERLINE' , '\033[4m'), ('ULINE' , '\033[4m')
    ])
    
    _bgs = OrderedDict([
        ('BLACK' , '\033[40m'),
        ('DARKRED' , '\033[41m'),
        ('DARKGREEN' , '\033[42m'),
        ('ORANGE' , '\033[43m'),
        ('DARKBLUE' , '\033[44m'),
        ('PURPLE' , '\033[45m'),
        ('DARKCYAN' , '\033[46m'),
        ('LIGHTGREY' , '\033[47m'), ('LIGHTGREY', '\033[47m'),
        
        ('DARKGREY' , '\033[100m'), ('DARKGRAY' , '\033[100m'),
        ('RED' , '\033[101m'),
        ('GREEN' , '\033[102m'),
        ('YELLOW' , '\033[103m'),
        ('BLUE' , '\033[104m'),
        ('MAGENTA' , '\033[105m'),
        ('CYAN' , '\033[106m'),
        ('GREY' , '\033[107m'), ('GRAY' , '\033[107m')
    ])
    
    _END = '\033[0m'

    _print = print
    
    @classmethod
    def colors(cls):
        """
Returns the list of named text colors in order.
        """
        return [k for k in cls._colors.keys() if k not in ['GRAY','DARKGRAY','LIGHTGRAY','BOLD','UNDERLINE','ULINE']]
    
    @classmethod
    def backgrounds(cls):
        """
Returns the list of named background colors in order.
        """
        return [k for k in cls._bgs.keys() if k not in ['GRAY','DARKGRAY','LIGHTGRAY']]
    
    @classmethod
    def reverse(cls,*args, **kwargs):
        """
Prints as white text on a black background.
        """
        if 'bg' in kwargs:
            del kwargs['bg']
        if 'ret' in kwargs and kwargs['ret']:
            return cls.print(255,*args,**kwargs,bg=232)
        else:
            cls.print(255,*args,**kwargs,bg=232)

    @classmethod
    def print(cls, clr=None, *args, bold=False, uline=False, ret=False, bg='', ignore=False, **kwargs):
        """
Parameters:
@clr: Sets text color. Value can either be
    str matching an entry in colorprinter.colors() or 'white', 'bold', or 'underline', or
    tuple (r,g,b): where r,g,b in [0,6), or
    int in [0,256): where [0,16) are colorprinter.colors() in order,
        [16,232) are tuple colors where clr = 16 + 36*r + 6*g + b, and
        [232,256) are greyscale from black to white
    Anything that's not a valid color will be treated as an arg. This include numpy.int64's.
object @args - positional: the things you want printed; str() is called on each arg

Optional[bool] @bold, @uline: if you want the color print bolded or underline respectively
Optional[bool] @ret: if you want the print string returned instead of printed
Optional @bg: Sets the background color. Values like @clr, but 'bold' and 'underline' not allowed.
Optional[bool] @ignore: If you want to regularly print functionality. Passes everything directly to the original print function.
    Setting @ignore true is equivalent to calling colorprinter._print().

All other kwargs are passed to colorprinter._print.
        """

        if clr is None and not args: # print empty line
            if not ret:
                cls._print(**kwargs)
            return
        elif clr is None:
            clr = args[0]
            if len(args) > 1:
                args = args[1:]

        if ignore: # check if regular print
            if args:
                if ret:
                    out = str(clr) + ' '
                    for i in args:
                        out += str(i) + ' '
                    return out[:-1]
                else:
                    cls._print(clr, *args, **kwargs)
                    return
            else:
                if ret:
                    return str(clr)
                else:
                    cls._print(clr, **kwargs)
                    return

        if 'sep' in kwargs and args:
            if not type(kwargs['sep']) is str:
                raise TypeError('sep must be None or a string, not ' + type(kwargs['sep']).__name__)
            sep = str(kwargs['sep'])
        else:
            sep = ' '

        out = ''
        colors = cls._colors # load this locally

        if type(clr) is str and not clr == '' and args:
            if clr.upper() == 'WHITE': # special case
                out += '\033[38;5;255m'
            elif clr.upper() in colors.keys(): # regular case
                out += colors[clr.upper()]
            else: # not a color
                out = str(clr) + sep

        elif type(clr) is tuple and args:
            if len(clr) == 3 and all([0 <= i < 6 for i in clr]): # regular case
                r,g,b = clr
                num = 16 + 36*r + 6*g + b
                out += '\033[38;5;' + str(num) + 'm'
            else: # not a color
                out = str(clr) + str(sep)

        elif type(clr) is int and args:
            if 0 <= clr < 256: # regular case
                out += '\033[38;5;' + str(clr) + 'm'
            else: # not a color
                out = str(clr) + sep

        else: # for anything else
            out = str(clr) + sep

        if bg: # asserts here because kwarg
            if type(bg) is str:
                assert bg.upper() in cls._bgs.keys(), 'Unknown background color'
                out += cls._bgs[bg.upper()]
            elif type(bg) is tuple:
                assert len(bg) == 3, 'Wrong length tuple given for background color'
                assert all([0 <= i < 6 for i in bg]), 'Background color rgb values must be [0,6)'
                r,g,b = bg
                num = 16 + 36*r + 6*g + b
                out += '\033[48;5;' + str(num) + 'm'
            elif type(bg) is int:
                if clr.upper() == 'WHITE':
                    out += '\033[48;5;255m'
                else:
                    assert 0 <= bg < 256, 'Background color in values must be [0,256)'
                    out += '\033[48;5;' + str(bg) + 'm'
            
        if bold:
            out = colors['BOLD'] + out
        if uline:
            out = colors['UNDERLINE'] + out
        
        if args:
            for i in args:
                out += str(i) + sep
            if len(sep):
                out = out[0:-len(sep)]

        if out[0] is '\033':
            out = out + cls._END
            
        if ret:
            return out
        else:
            cls._print(out, **kwargs)

# switch the print function
print = colorprinter.print
