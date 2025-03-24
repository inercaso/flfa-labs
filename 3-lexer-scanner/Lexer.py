from Tokens import Token, TokenType

class Position:
    def __init__(self, line, col):
        self.line = line
        self.col = col
    
    def advance(self, char=None):
        self.col += 1
        return self
    
    def advance_line(self):
        self.line += 1
        self.col = 0
        return self
    
    def copy(self):
        return Position(self.line, self.col)
    
    def __str__(self):
        return f"({self.line}:{self.col})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(1, 0)  # line 1, column 0
        self.current_char = None
        self.advance()
    
    def advance(self):
        """advance the current character position"""
        if self.pos.col < len(self.text):
            self.current_char = self.text[self.pos.col]
            self.pos.advance()
        else:
            self.current_char = None
    
    def peek(self, n=1):
        """peek n characters ahead without advancing"""
        peek_pos = self.pos.col + n - 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None
    
    def skip_whitespace(self):
        """skip whitespace characters"""
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.pos.advance_line()
            self.advance()
    
    def skip_comment(self):
        """skip a line comment starting with //"""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        
        if self.current_char == '\n':
            self.pos.advance_line()
            self.advance()
    
    def collect_number(self):
        """collect a number (integer or float)"""
        result = ''
        is_float = False
        start_pos = self.pos.copy()
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if is_float:  # second decimal point is not allowed
                    break
                is_float = True
            result += self.current_char
            self.advance()
        
        if is_float:
            return Token(TokenType.DURATION, float(result), start_pos)
        return Token(TokenType.DURATION, int(result), start_pos)
    
    def collect_identifier(self):
        """collect an identifier or a command"""
        start_pos = self.pos.copy()
        result = ''
        
        if self.current_char == '\\':
            result += self.current_char
            self.advance()
            while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                result += self.current_char
                self.advance()
            return Token(TokenType.COMMAND, result, start_pos)
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # check for note tokens
        if result.lower() in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            return Token(TokenType.NOTE, result.lower(), start_pos)
        elif result.lower() == 'r':
            return Token(TokenType.REST, result.lower(), start_pos)
        
        # check for dynamics
        if result.lower() in ['pp', 'p', 'mp', 'mf', 'f', 'ff']:
            return Token(TokenType.DYNAMIC, result.lower(), start_pos)
        
        # otherwise it's an identifier
        return Token(TokenType.IDENTIFIER, result, start_pos)
    
    def tokenize(self):
        """tokenize the input text"""
        tokens = []
        
        while self.current_char is not None:
            # handle whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # handle comments
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
            
            # handle numbers
            if self.current_char.isdigit():
                tokens.append(self.collect_number())
                continue
            
            # handle notes, rests, and identifiers
            if self.current_char.isalpha() or self.current_char == '_' or self.current_char == '\\':
                tokens.append(self.collect_identifier())
                continue
            
            # handle special symbols
            current_pos = self.pos.copy()
            
            if self.current_char == '#':
                tokens.append(Token(TokenType.SHARP, '#', current_pos))
            elif self.current_char == 'b' and not self.peek().isalnum():
                tokens.append(Token(TokenType.FLAT, 'b', current_pos))
            elif self.current_char == '.':
                tokens.append(Token(TokenType.DOT, '.', current_pos))
            elif self.current_char == '~':
                tokens.append(Token(TokenType.TRIPLET, '~', current_pos))
            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS, '+', current_pos))
            elif self.current_char == '-':
                tokens.append(Token(TokenType.MINUS, '-', current_pos))
            elif self.current_char == '=':
                tokens.append(Token(TokenType.EQUALS, '=', current_pos))
            elif self.current_char == '(':
                tokens.append(Token(TokenType.LPAREN, '(', current_pos))
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RPAREN, ')', current_pos))
            elif self.current_char == '{':
                tokens.append(Token(TokenType.LBRACE, '{', current_pos))
            elif self.current_char == '}':
                tokens.append(Token(TokenType.RBRACE, '}', current_pos))
            elif self.current_char == ',':
                tokens.append(Token(TokenType.COMMA, ',', current_pos))
            elif self.current_char == '|':
                if self.peek() == ':':
                    tokens.append(Token(TokenType.REPEAT_START, '|:', current_pos))
                    self.advance()  # consume the extra character
                else:
                    tokens.append(Token(TokenType.BAR, '|', current_pos))
            elif self.current_char == ':' and self.peek() == '|':
                tokens.append(Token(TokenType.REPEAT_END, ':|', current_pos))
                self.advance()  # consume the extra character
            else:
                # unknown character
                tokens.append(Token(TokenType.ERROR, self.current_char, current_pos))
            
            self.advance()
        
        # add EOF token
        tokens.append(Token(TokenType.EOF, None, self.pos.copy()))
        return tokens 
