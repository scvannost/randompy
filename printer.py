from collections import OrderedDict
import sys as _sys

class colorprinter:
    """
A class to print in fun colors/styles with.
Methods:
    colors: returns the list of possible text colors in order
    backgrounds: returns the list of possible background colors in order
    reverse: uses print to make a white font on a black background
    print: extends the regular print function with fun add-ons; see print.__doc__
    _print: the original print function.
Properties:
    bool UNICODE_SUPPORT: whether or not stdout supports unicode
    """
    UNICODE_SUPPORT = _sys.stdout.encoding.lower().startswith('utf-')

    _colors = OrderedDict([ # a library of all the things
        ('BLACK',		'\033[30m'),
        ('DARKRED',		'\033[31m'),
        ('DARKGREEN',	'\033[32m'),
        ('ORANGE',		'\033[33m'),
        ('DARKBLUE',	'\033[34m'),
        ('PURPLE',		'\033[35m'),
        ('DARKCYAN',	'\033[36m'),
        ('LIGHTGREY',	'\033[37m'),	('LIGHTGRAY',	'\033[37m'),
        
        ('DARKGREY',	'\033[90m'),	('DARKGRAY',	'\033[90m'),
        ('RED',			'\033[91m'),
        ('GREEN',		'\033[92m'),
        ('YELLOW',		'\033[93m'),
        ('BLUE',		'\033[94m'),
        ('MAGENTA',		'\033[95m'),
        ('CYAN',		'\033[96m'),
        ('GREY',		'\033[97m'),	('GRAY',		'\033[97m'),
        
        ('BOLD',		'\033[1m'),
        ('UNDERLINE',	'\033[4m'),		('ULINE',		'\033[4m')
    ])
    
    _bgs = OrderedDict([
        ('BLACK',		'\033[40m'),
        ('DARKRED', 	'\033[41m'),
        ('DARKGREEN',	'\033[42m'),
        ('ORANGE',		'\033[43m'),
        ('DARKBLUE',	'\033[44m'),
        ('PURPLE',		'\033[45m'),
        ('DARKCYAN',	'\033[46m'),
        ('LIGHTGREY',	'\033[47m'),	('LIGHTGREY',	'\033[47m'),
        
        ('DARKGREY',	'\033[100m'),	('DARKGRAY',	'\033[100m'),
        ('RED',			'\033[101m'),
        ('GREEN',		'\033[102m'),
        ('YELLOW',		'\033[103m'),
        ('BLUE',		'\033[104m'),
        ('MAGENTA',		'\033[105m'),
        ('CYAN',		'\033[106m'),
        ('GREY',		'\033[107m'),	('GRAY',		'\033[107m')
    ])

    _LATEX = {
    	# greek
    	'\\Alpha'  : 'Α',	'\\alpha'    : 'α',	'\\Beta'     : 'Β',	'\\beta'	: 'β',
    	'\\Gamma'  : 'Γ',	'\\gamma'    : 'γ',	'\\Delta'    : 'Δ',	'\\delta'	: 'δ',
    	'\\Epsilon': 'Ε',	'\\epsilon'  : 'ε',	'\\Zeta'     : 'Ζ',	'\\zeta'	: 'ζ',
    	'\\Eta'    : 'Η',	'\\eta'      : 'η',	'\\Theta'    : 'Θ',	'\\theta'	: 'θ',
    	'\\Iota'   : 'Ι',	'\\iota'     : 'ι',	'\\Kappa'    : 'Κ',	'\\kappa'	: 'κ',
    	'\\Lambda' : 'Λ',	'\\lambda'   : 'λ',	'\\Mu'       : 'Μ',	'\\mu'		: 'μ',
    	'\\Nu'     : 'Ν',	'\\nu'       : 'ν',	'\\Xi'       : 'Ξ',	'\\xi'		: 'ξ',
    	'\\Omicron': 'Ο',	'\\omicron'  : 'ο',	'\\Pi'       : 'Π',	'\\pi'		: 'π',
    	'\\Rho'    : 'Ρ',	'\\rho'      : 'ρ',	'\\Sigma'    : 'Σ',	'\\sigma'	: 'σ',	'\\finalsigma' : 'ς',
    	'\\Tau'    : 'Τ',	'\\tau'      : 'τ',	'\\Upsilon'  : 'Υ',	'\\upsilon'	: 'υ',
    	'\\Phi'    : 'Φ',	'\\phi'      : 'φ',	'\\Chi'      : 'Χ',	'\\chi'		: 'χ',
    	'\\Psi'    : 'Ψ',	'\\psi'      : 'ψ',	'\\Omega'    : 'Ω',	'\\omega'	: 'ω',

    	# Hebrew
    	'\\aleph'  : 'ℵ ',

    	# Symbols
    	'\\dagger' : '†',	'\\dbldagger': '‡',	'\\section'  : '§',	'\\paragraph'   : '¶',
    	'\\bullet' : '∙',	'\\dotprod'  : '∙',	'\\em'       : '—',
    	'\\en'     : '–',	'\\pounds'   : '£',	'\\euro'     : '€',
    	'\\yen'    : '¥',	'\\yuan'     : '¥',	'\\won'      : '₩ ',	'\\cents'       : '¢',
    	'\\check'  : '✓ ',	'\\tick'     : '✓ ', '\\copyright': '©',	'\\registered'  : '®',
    	'\\tm'     : '™',	'\\trademark': '™', '\\sm'       : '℠ ',	'\\servicemark' : '℠ ',
    	'\\flat'   : '♭',	'\\natural'  : '♮',	'\\sharp'    : '♯',	'\\!': '¡', '\\?': '¿',

    	# Math
    	'\\divide'   : '÷',	'\\cross'    : '×', '\\union'    : '∪ ', '\\intersection'  : '∩ ',
    	'\\or'       : '∨ ',	'\\and'      : '∧ ', '\\plusminus': '±', '\\minusplus'     : '∓ ',
    	'\\approx'   : '≈',	'\\integral' : '∫', '\\closedintegral': '∮',
    	'\\dblintegral':'∬ ', '\\triintegral': '∭ ',
    	'\\therefore': '∴ ',	'\\because'  : '∵ ',	'\\not'      : '¬', '\\proportional'  : '∝ ',
    	'\\infinity' : '∞',	'\\sqrt'     : '√', '\\qed'     : '■ ',	'\\QED'  : '■ ',
    	'\\ne'       : '≠',	'\\iff'      : '⇔ ',	'\\dblarrow': '↔ ',
    	'\\nabla'    : '∇ ',	'\\grad'     : '∇ ',	'\\empty'    : '∅ ', '\\nullset': '∅ ',
    	'\\sum'      : 'Σ',	'\\product'  : 'Π', '\\element'      : '∈ ',	'\\elementnot': '∉ ',
    	'\\exists'   : '∃ ',	'\\forall'   : '∀ ',	'\\partial'  : '∂', '\\{'    : '⟨',	'\\}' : '⟩',
    	'\\lfloor'   : '⌊',	'\\rfloor'   : '⌋', '\\lceil'    : '⌈',	'\\rceil'   : '⌉',	'\\norm' : '‖',
    	'\\abs'      : '|',	'\\leftarrow': '← ', '\\rightarrow': '→ ','\\leq'     : '≤',	'\\geq'  : '≥',
    	'\\ll'       : '≪ ','\\dblless' : '≪ ','\\gg'       : '≫ ','\\dblgreater': '≫ ',
    	'\\triless'  : '⋘  ', '\\veryless' : '⋘  ', '\\trigreater'    : '⋙  ','\\verygreater'   : '⋙  ',
    	'\\triequal' : '≡ ',	'\\prime'     : '′','\\dblprime' : '″','\\triprime' : '‴',
    	'\\defined'  : '≜ ',	'\\definition': '≝ ','\\congruent': '≅ ',	'\\ddots'   : '⋱ ',	'\\vdots': '⋮ ',
    	'\\angstrom' : 'Å ',	'\\degree'    : '°','\\degC'     : '℃  ', '\\degF'    : '℉ ',	'\\hbar': 'ℏ ',

    	# double struck
    	'\\zz': 'ℤ ',	'\\uu': '𝕌 ',	'\\rr': 'ℝ ',	'\\qq': 'ℚ ',	'\\pp': 'ℙ ',
    	'\\nn': 'ℕ ',	'\\hh': 'ℍ ',	'\\ee': '𝔼 ',	'\\cc': 'ℂ ',	'\\bb': '𝔹 ',
    	
    	# combining
    	'\\grave'  : '\u0300',	'\\accent': '\u0301',	'\\acute' : '\u0301',	'\\hat'      : '\u0302',	'\\tilde'    : '\u0303',
    	'\\bar'    : '\u0305',	'\\overdot'   : '\u0307',	'\\dbldot': '\u0308',	'\\tridot': '\u20DB',	'\\quaddot'  : '\u20DC',
    	'\\cedilla': '\u0327',	'\\overleft'  : '\u20D0',	'\\vector': '\u20D1',	'\\overright'    : '\u20D1', 	'\\overlr': '\u20E1',
    	'\\underright': '\u20ED','\\underleft': '\u20EC',

    }
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
        return cls.print(255,*args,**kwargs,bg=232)

    @classmethod
    def print(cls, clr=None, *args, bold=False, uline=False, ret=False, bg='', ignore=False, **kwargs):
        """
Parameters:
@clr: Sets text color. Value can either be
    str matching an entry in colorprinter.colors() or 'white', 'bold', or 'underline'/'uline', or
    tuple (r,g,b): where r,g,b in [0,6), or
    int in [0,256): where [0,16) are colorprinter.colors() in order,
        [16,232) are tuple colors where clr = 16 + 36*r + 6*g + b, and
        [232,256) are greyscale from black to white
    Anything that's not a valid color will be treated as an arg. This include np.int64's.
object @args - positional: the things you want printed; str() is called on each arg

Optional[bool] @bold, @uline: if you want the color print bolded or underline respectively
Optional[bool] @ret: if you want the print string returned instead of printed
Optional @bg: Sets the background color. Values like @clr, but 'bold' and 'underline' not allowed.
Optional[bool] @ignore: If you want to regularly print functionality. Passes everything directly to the original print function. @ret still applies.

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
        # load these locally
        colors = cls._colors
        LATEX = cls._LATEX

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

        if cls.UNICODE_SUPPORT:
        # text substitutions go in here
            if '\\' in out:
                for k,v in LATEX.items():
                    temp = out.split(k)
                    if len(temp) > 1:
                        if not jp or v[-1] != ' ':
                            out = v.join(temp)
                        else:
                            out = v.strip().join(temp)

            if '(C)' in out or '(c)' in out:
                temp = out.split('(C)')
                if len(temp) > 1:
                    out = '©'.join(temp)
                else:
                    temp = out.split('(c)')
                    out = '©'.join(temp)

            if '(R)' in out or '(r)' in out:
                temp = out.split('(R)')
                if len(temp) > 1:
                    out = '®'.join(temp)

        if '\(' in out:
            out = out.replace('\(','(')
            
        if ret:
            return out
        else:
            cls._print(out, **kwargs)

# switch the print function
print = colorprinter.print
