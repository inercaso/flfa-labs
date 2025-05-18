from enum import Enum, auto
from typing import List, Optional

class NodeType(Enum):
    # Music structure nodes
    SCORE = auto()         # Root node for the entire score
    BAR = auto()           # Bar line
    REPEAT = auto()        # Repeat section
    
    # Note-related nodes
    NOTE = auto()          # Musical note
    REST = auto()          # Rest
    CHORD = auto()         # Multiple notes played together
    
    # Expression nodes
    DYNAMIC = auto()       # Dynamic marking (p, f, mf, etc.)
    TEMPO = auto()         # Tempo marking
    
    # Command nodes
    COMMAND = auto()       # Special command
    
    # Expression nodes
    BINARY_OP = auto()     # Binary operation (for transposition)
    UNARY_OP = auto()      # Unary operation
    
    # Value nodes
    NUMBER = auto()        # Numeric value
    IDENTIFIER = auto()    # Variable name

class ASTNode:
    def __init__(self, node_type: NodeType, value: Optional[str] = None):
        self.type = node_type
        self.value = value
        self.children: List[ASTNode] = []
        self._parent = None
    
    def add_child(self, child: 'ASTNode') -> None:
        self.children.append(child)
        child._parent = self
    
    def is_last_child(self) -> bool:
        if not self._parent:
            return True
        return self._parent.children[-1] == self
    
    def __str__(self, level: int = 0) -> str:
        # For root node, don't add any prefix
        if level == 0:
            ret = f"{self.type.name}"
            if self.value is not None:
                ret += f": {self.value}"
            ret += "\n"
        else:
            # For all other nodes, add proper tree structure
            prefix = "│   " * (level - 1)
            if level > 0:
                prefix += "└── " if self.is_last_child() else "├── "
            ret = prefix + f"{self.type.name}"
            if self.value is not None:
                ret += f": {self.value}"
            ret += "\n"
        
        # Add children with proper indentation
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class NoteNode(ASTNode):
    def __init__(self, pitch: str, octave: int, duration: float, modifiers: List[str] = None):
        super().__init__(NodeType.NOTE)
        self.pitch = pitch
        self.octave = octave
        self.duration = duration
        self.modifiers = modifiers or []
    
    def __str__(self, level: int = 0) -> str:
        if level == 0:
            ret = f"{self.type.name}"
            ret += f": {self.pitch}{self.octave} ({self.duration})"
            if self.modifiers:
                ret += f" {''.join(self.modifiers)}"
            ret += "\n"
        else:
            prefix = "│   " * (level - 1)
            if level > 0:
                prefix += "└── " if self.is_last_child() else "├── "
            ret = prefix + f"{self.type.name}"
            ret += f": {self.pitch}{self.octave} ({self.duration})"
            if self.modifiers:
                ret += f" {''.join(self.modifiers)}"
            ret += "\n"
        
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class RestNode(ASTNode):
    def __init__(self, duration: float):
        super().__init__(NodeType.REST)
        self.duration = duration
    
    def __str__(self, level: int = 0) -> str:
        if level == 0:
            ret = f"{self.type.name}"
            ret += f": {self.duration}"
            ret += "\n"
        else:
            prefix = "│   " * (level - 1)
            if level > 0:
                prefix += "└── " if self.is_last_child() else "├── "
            ret = prefix + f"{self.type.name}"
            ret += f": {self.duration}"
            ret += "\n"
        
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class BarNode(ASTNode):
    def __init__(self):
        super().__init__(NodeType.BAR)
    
    def __str__(self, level: int = 0) -> str:
        if level == 0:
            ret = f"{self.type.name}\n"
        else:
            prefix = "│   " * (level - 1)
            if level > 0:
                prefix += "└── " if self.is_last_child() else "├── "
            ret = prefix + f"{self.type.name}\n"
        
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class RepeatNode(ASTNode):
    def __init__(self):
        super().__init__(NodeType.REPEAT, "2x")
    
    def __str__(self, level: int = 0) -> str:
        if level == 0:
            ret = f"{self.type.name}"
            if self.value is not None:
                ret += f": {self.value}"
            ret += "\n"
        else:
            prefix = "│   " * (level - 1)
            if level > 0:
                prefix += "└── " if self.is_last_child() else "├── "
            ret = prefix + f"{self.type.name}"
            if self.value is not None:
                ret += f": {self.value}"
            ret += "\n"
        
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class DynamicNode(ASTNode):
    def __init__(self, dynamic: str):
        super().__init__(NodeType.DYNAMIC, dynamic)
    
    def __str__(self, level: int = 0) -> str:
        if level == 0:
            ret = f"{self.type.name}"
            if self.value is not None:
                ret += f": {self.value}"
            ret += "\n"
        else:
            prefix = "│   " * (level - 1)
            if level > 0:
                prefix += "└── " if self.is_last_child() else "├── "
            ret = prefix + f"{self.type.name}"
            if self.value is not None:
                ret += f": {self.value}"
            ret += "\n"
        
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class TempoNode(ASTNode):
    def __init__(self, bpm: int):
        super().__init__(NodeType.TEMPO, f"{bpm} BPM")
    
    def __str__(self, level: int = 0) -> str:
        if level == 0:
            ret = f"{self.type.name}"
            if self.value is not None:
                ret += f": {self.value}"
            ret += "\n"
        else:
            prefix = "│   " * (level - 1)
            if level > 0:
                prefix += "└── " if self.is_last_child() else "├── "
            ret = prefix + f"{self.type.name}"
            if self.value is not None:
                ret += f": {self.value}"
            ret += "\n"
        
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret 