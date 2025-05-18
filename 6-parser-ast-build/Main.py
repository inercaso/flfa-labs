import os
import time
from typing import List
from Tokens import Token, TokenType
from Parser import Parser
from AST import ASTNode, NodeType, NoteNode, RestNode, BarNode, RepeatNode, DynamicNode, TempoNode
import re

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
    
    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, None, self.line))
        return self.tokens
    
    def scan_token(self):
        c = self.advance()
        
        # Note patterns
        if re.match(r'[a-g]', c):
            self.add_token(TokenType.NOTE, c)
        elif c == 'r':
            self.add_token(TokenType.REST)
        
        # Modifiers
        elif c == '#':
            self.add_token(TokenType.SHARP, c)
        elif c == 'b':
            self.add_token(TokenType.FLAT, c)
        
        # Octave markers
        elif c.isdigit():
            self.number()
        elif c == '+':
            self.add_token(TokenType.OCTAVE_UP, c)
        elif c == '-':
            self.add_token(TokenType.OCTAVE_DOWN, c)
        
        # Duration markers
        elif c == '.':
            self.add_token(TokenType.DOT, c)
        elif c == '~':
            self.add_token(TokenType.TRIPLET, c)
        
        # Structure
        elif c == '|':
            if self.match(':'):
                self.add_token(TokenType.REPEAT_START)
            else:
                self.add_token(TokenType.BAR)
        elif c == ':':
            if self.match('|'):
                self.add_token(TokenType.REPEAT_END)
        
        # Dynamics
        elif c in 'pfm':
            self.dynamic()
        
        # Commands
        elif c == '\\':
            self.command()
        
        # Whitespace
        elif c in ' \t\r':
            pass
        elif c == '\n':
            self.line += 1
        else:
            print(f"Warning: Unexpected character '{c}' at line {self.line}")
    
    def number(self):
        while self.peek().isdigit():
            self.advance()
        
        number = self.source[self.start:self.current]
        if self.previous() == '0':
            self.add_token(TokenType.OCTAVE, number)
        else:
            self.add_token(TokenType.DURATION, number)
    
    def command(self):
        command = ""
        while self.peek().isalnum() or self.peek() == '_':
            command += self.advance()
        self.add_token(TokenType.COMMAND, command)
    
    def dynamic(self):
        dynamic = self.source[self.start:self.current]
        while self.peek().isalpha():
            dynamic += self.advance()
        self.add_token(TokenType.DYNAMIC, dynamic)
    
    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        
        self.current += 1
        return True
    
    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    
    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c
    
    def add_token(self, type: TokenType, value: str = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, value or text, self.line))
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def previous(self) -> str:
        return self.source[self.current - 1]

def process_source(source: str):
    start_time = time.time()
    
    print("\n\033[1;35m=== Starting Lexical Analysis ===\033[0m")
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    lex_time = time.time() - start_time
    print(f"Lexical analysis completed in {lex_time:.3f} seconds")
    
    print("\n\033[1;35m=== Tokens Generated ===\033[0m")
    for token in tokens:
        print(token)
    
    print("\n\033[1;35m=== Starting Parsing ===\033[0m")
    parse_start = time.time()
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        parse_time = time.time() - parse_start
        print(f"\n\033[1;35m=== Parsing Complete in {parse_time:.3f} seconds ===\033[0m")
        print("\n\033[1;35m=== Abstract Syntax Tree ===\033[0m")
        if ast is None:
            print("Error: Parser returned None")
        else:
            print(str(ast))
        total_time = time.time() - start_time
        print(f"\nTotal processing time: {total_time:.3f} seconds")
    except SyntaxError as e:
        print(f"\033[1;31mSyntax Error: {e}\033[0m")
    except Exception as e:
        print(f"\033[1;31mUnexpected Error: {e}\033[0m")
        import traceback
        traceback.print_exc()

def show_help():
    print("\n\033[1;36m=== Music Notation Help ===\033[0m")
    print("\033[1;33mBasic Elements:\033[0m")
    print("  Notes: a, b, c, d, e, f, g")
    print("  Octaves: 4 (middle C), 5 (higher), 3 (lower)")
    print("  Duration: 4 (quarter note), 8 (eighth note), 16 (sixteenth note)")
    print("\n\033[1;33mModifiers:\033[0m")
    print("  # - Sharp")
    print("  b - Flat")
    print("  . - Dotted note (1.5x duration)")
    print("  ~ - Triplet (2/3x duration)")
    print("\n\033[1;33mStructure:\033[0m")
    print("  | - Bar line")
    print("  |: :| - Repeat section")
    print("\n\033[1;33mDynamics:\033[0m")
    print("  p - Piano (soft)")
    print("  f - Forte (loud)")
    print("  mf - Mezzo-forte (medium loud)")
    print("\n\033[1;33mCommands:\033[0m")
    print("  \\bpm 120 - Set tempo to 120 BPM")
    print("\n\033[1;33mExample:\033[0m")
    print("  \\bpm 120")
    print("  mf")
    print("  c4 4 | d4 4 | e4 4 | f4 4 |")
    print("  |: g4 4 | a4 4 | b4 4 | c5 4 :|")
    print("  p")
    print("  c5 4 | b4 4 | a4 4 | g4 4 |")
    input("\n\033[1;32mPress Enter to continue...\033[0m")

def get_input_with_suggestions(prompt: str, suggestions: List[str]) -> str:
    print(f"\033[1;32m{prompt}\033[0m")
    print("\033[1;33mSuggestions:\033[0m")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")
    print("  Or type your own input")
    return input("\033[1;32mYour choice: \033[0m")

def main():
    while True:
        print("\033[1;36m=== Music Notation Parser ===\033[0m")
        print("\033[1;33m1. Parse from file")
        print("2. Parse from input")
        print("3. Help")
        print("4. Exit\033[0m")
        
        choice = input("\033[1;32mEnter your choice: \033[0m")
        
        if choice == "1":
            suggestions = [
                "sample_music.txt",
                "my_music.txt",
                "scale.txt",
                "tree_example.txt"
            ]
            filename = get_input_with_suggestions("Enter filename:", suggestions)
            try:
                # Try to open the file in the current directory
                with open(filename, 'r') as f:
                    source = f.read()
                process_source(source)
            except FileNotFoundError:
                print(f"\033[1;31mFile '{filename}' not found in current directory!\033[0m")
                print("Available files:")
                for file in os.listdir('.'):
                    if file.endswith('.txt'):
                        print(f"  - {file}")
        
        elif choice == "2":
            print("\033[1;36m=== Music Notation Input ===\033[0m")
            print("\033[1;33mTemplate:\033[0m")
            print("  \\bpm 120")
            print("  mf")
            print("  c4 4 | d4 4 | e4 4 | f4 4 |")
            print("  |: g4 4 | a4 4 | b4 4 | c5 4 :|")
            print("  p")
            print("  c5 4 | b4 4 | a4 4 | g4 4 |")
            print("\n\033[1;32mEnter your music notation (type 'END' on a new line to finish):\033[0m")
            print("\033[1;33mQuick templates (type number to use):\033[0m")
            print("  1. C Major Scale")
            print("  2. Simple Melody")
            print("  3. Tree Example")
            print("  4. Empty Template")
            
            template_choice = input("\033[1;32mChoose template (or press Enter to start typing): \033[0m")
            
            if template_choice == "1":
                source = """\\bpm 120
mf
c4 4 | d4 4 | e4 4 | f4 4 |
g4 4 | a4 4 | b4 4 | c5 4 |
c5 4 | b4 4 | a4 4 | g4 4 |
f4 4 | e4 4 | d4 4 | c4 4 |"""
            elif template_choice == "2":
                source = """\\bpm 100
mf
c4 4 | e4 4 | g4 4 | c5 4 |
e5 4 | c5 4 | g4 4 | e4 4 |
c4 4 | r4 4 | c4 4 | r4 4 |"""
            elif template_choice == "3":
                source = """\\bpm 120
mf
c4 4 | d4 4 | e4 4 | f4 4 |
|: g4 4 | a4 4 | b4 4 | c5 4 :|
p
c5 4 | b4 4 | a4 4 | g4 4 |"""
            elif template_choice == "4":
                source = """\\bpm 120
mf
| | | |"""
            else:
                lines = []
                while True:
                    line = input()
                    if line == "END":
                        break
                    lines.append(line)
                source = "\n".join(lines)
            
            process_source(source)
        
        elif choice == "3":
            show_help()
        
        elif choice == "4":
            print("\033[1;33mGoodbye!\033[0m")
            break
        
        else:
            print("\033[1;31mInvalid choice!\033[0m")

if __name__ == "__main__":
    main() 