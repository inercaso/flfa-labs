from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class TokenType(Enum):
    # Basic elements
    NOTE = auto()          # a, b, c, d, e, f, g
    REST = auto()          # r
    
    # Modifiers
    SHARP = auto()         # #
    FLAT = auto()          # b
    DOT = auto()           # .
    TRIPLET = auto()       # ~
    
    # Octave markers
    OCTAVE = auto()        # 4, 5, 3
    OCTAVE_UP = auto()     # +
    OCTAVE_DOWN = auto()   # -
    
    # Duration markers
    DURATION = auto()      # 4, 8, 16
    
    # Structure
    BAR = auto()           # |
    REPEAT_START = auto()  # |:
    REPEAT_END = auto()    # :|
    
    # Dynamics
    DYNAMIC = auto()       # p, f, mf
    
    # Commands
    COMMAND = auto()       # \bpm, etc.
    
    # Special
    EOF = auto()           # End of file

@dataclass
class Token:
    type: TokenType
    value: Optional[str]
    line: int
    
    def __str__(self) -> str:
        if self.value is None:
            return f"Token({self.type.name}, None, line={self.line})"
        return f"Token({self.type.name}, '{self.value}', line={self.line})" 