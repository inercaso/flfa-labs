from typing import List, Optional
from AST import *
from Tokens import Token, TokenType

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.root = ASTNode(NodeType.SCORE)
        self.current_section = self.root
        self.current_bar = None
    
    def parse(self) -> ASTNode:
        print("Building AST...")
        while not self.is_at_end():
            node = self.parse_statement()
            if node:
                print(f"Added node: {node.type.name}")
                if isinstance(node, BarNode):
                    if self.current_bar:
                        self.current_section.add_child(self.current_bar)
                    self.current_bar = node
                elif isinstance(node, (DynamicNode, TempoNode)):
                    if self.current_bar:
                        self.current_section.add_child(self.current_bar)
                        self.current_bar = None
                    self.root.add_child(node)
                elif isinstance(node, (NoteNode, RestNode)):
                    if self.current_bar:
                        self.current_bar.add_child(node)
                    else:
                        self.current_bar = BarNode()
                        self.current_bar.add_child(node)
                elif isinstance(node, RepeatNode):
                    if self.current_bar:
                        self.current_section.add_child(self.current_bar)
                        self.current_bar = None
                    self.root.add_child(node)
                    self.current_section = node
            else:
                self.advance()
        
        if self.current_bar:
            self.current_section.add_child(self.current_bar)
        
        print("AST construction complete")
        return self.root
    
    def parse_statement(self) -> Optional[ASTNode]:
        if self.match(TokenType.NOTE):
            print("Parsing note...")
            return self.parse_note()
        elif self.match(TokenType.REST):
            print("Parsing rest...")
            return self.parse_rest()
        elif self.match(TokenType.BAR):
            print("Parsing bar...")
            return BarNode()
        elif self.match(TokenType.REPEAT_START):
            print("Parsing repeat section...")
            repeat_node = self.parse_repeat()
            self.current_section = self.root
            self.current_bar = None
            return repeat_node
        elif self.match(TokenType.DYNAMIC):
            print(f"Parsing dynamic: {self.previous().value}")
            return DynamicNode(self.previous().value)
        elif self.match(TokenType.COMMAND):
            print(f"Parsing command: {self.previous().value}")
            return self.parse_command()
        elif self.match(TokenType.DURATION):  # Handle standalone duration tokens
            print(f"Skipping standalone duration: {self.previous().value}")
            return None
        return None
    
    def parse_note(self) -> NoteNode:
        token = self.previous()
        pitch = token.value
        octave = 4  # default octave
        duration = 1.0  # default duration
        modifiers = []
        
        # Parse octave
        if self.match(TokenType.OCTAVE):
            octave = int(self.previous().value)
        elif self.match(TokenType.OCTAVE_UP):
            octave += 1
        elif self.match(TokenType.OCTAVE_DOWN):
            octave -= 1
        
        # Parse duration
        if self.match(TokenType.DURATION):
            duration = 1.0 / int(self.previous().value)
            if self.match(TokenType.DOT):
                duration *= 1.5
            if self.match(TokenType.TRIPLET):
                duration *= 2/3
        
        # Parse modifiers
        while self.match(TokenType.SHARP) or self.match(TokenType.FLAT):
            modifiers.append(self.previous().value)
        
        return NoteNode(pitch, octave, duration, modifiers)
    
    def parse_rest(self) -> RestNode:
        duration = 1.0  # default duration
        
        if self.match(TokenType.DURATION):
            duration = 1.0 / int(self.previous().value)
            if self.match(TokenType.DOT):
                duration *= 1.5
            if self.match(TokenType.TRIPLET):
                duration *= 2/3
        
        return RestNode(duration)
    
    def parse_repeat(self) -> RepeatNode:
        repeat_node = RepeatNode()
        previous_section = self.current_section
        previous_bar = self.current_bar
        self.current_section = repeat_node
        self.current_bar = None
        
        # Keep track of tokens to detect unclosed repeat
        start_pos = self.current
        
        while not self.match(TokenType.REPEAT_END):
            if self.is_at_end():
                # If we reach the end without finding a repeat end, 
                # rewind to the start of the repeat and parse as normal
                self.current = start_pos
                self.current_section = previous_section
                self.current_bar = previous_bar
                return None
            
            node = self.parse_statement()
            if node:
                if isinstance(node, BarNode):
                    if self.current_bar:
                        self.current_section.add_child(self.current_bar)
                    self.current_bar = node
                elif isinstance(node, (NoteNode, RestNode)):
                    if self.current_bar:
                        self.current_bar.add_child(node)
                    else:
                        self.current_bar = BarNode()
                        self.current_bar.add_child(node)
                else:
                    self.current_section.add_child(node)
            else:
                self.advance()
        
        # Add any remaining bar in the repeat section
        if self.current_bar:
            self.current_section.add_child(self.current_bar)
        
        self.current_section = previous_section
        self.current_bar = previous_bar
        return repeat_node
    
    def parse_command(self) -> ASTNode:
        command = self.previous().value
        if command == "\\bpm":
            if not self.match(TokenType.DURATION):
                raise SyntaxError("Expected BPM value after \\bpm command")
            return TempoNode(int(self.previous().value))
        return ASTNode(NodeType.COMMAND, command)
    
    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1] 