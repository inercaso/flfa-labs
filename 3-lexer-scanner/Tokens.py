from enum import Enum, auto

class TokenType(Enum):
    # note types
    NOTE = auto()          # a, b, c, d, e, f, g
    REST = auto()          # r (rest)
    
    # note modifiers
    SHARP = auto()         # #
    FLAT = auto()          # b
    
    # octave markers
    OCTAVE = auto()        # number indicating octave (e.g., 4)
    OCTAVE_UP = auto()     # + (raise octave)
    OCTAVE_DOWN = auto()   # - (lower octave)
    
    # duration markers
    DURATION = auto()      # number for duration (e.g., 1, 4, 8, 16)
    DOT = auto()           # . (dotted note)
    TRIPLET = auto()       # ~ (triplet)
    
    # control symbols
    TEMPO = auto()         # tempo command (bpm)
    DYNAMIC = auto()       # dynamics (p, f, mf, etc.)
    
    # structure
    BAR = auto()           # | (bar line)
    REPEAT_START = auto()  # |: (repeat start)
    REPEAT_END = auto()    # :| (repeat end)
    
    # mathematical operations for transposition
    PLUS = auto()          # + (for transposition)
    MINUS = auto()         # - (for transposition)
    
    # special commands
    COMMAND = auto()       # special command starting with \
    
    # misc
    IDENTIFIER = auto()    # variable name
    EQUALS = auto()        # = (assignment)
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    COMMA = auto()         # ,
    
    # end of file
    EOF = auto()           # end of file
    
    # error
    ERROR = auto()         # lexical error

class Token:
    def __init__(self, token_type, value=None, position=None):
        self.type = token_type
        self.value = value
        self.position = position
    
    def __str__(self):
        if self.value is not None:
            return f"Token({self.type}, '{self.value}', pos={self.position})"
        return f"Token({self.type}, pos={self.position})"
    
    def __repr__(self):
        return self.__str__() 