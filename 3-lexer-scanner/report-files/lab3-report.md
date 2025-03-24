# Laboratory Work #3: Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Daniela Cebotari, FAF-231
### Professors: Cretu Dumitru, Irina Cojuhari

----

## Theory

Lexical analysis, often performed by a lexer (also known as a scanner or tokenizer), is the first phase of a compiler or interpreter. Its main purpose is to convert a sequence of characters into a sequence of tokens - the basic meaningful units of a source program.

The lexer reads input characters one at a time, identifies patterns, and produces tokens. A token is a pair consisting of a token type and an optional token value. For example, in a typical programming language, token types might include identifiers, keywords, operators, and literals.

Lexical analysis is typically implemented using finite automata. Each pattern to be recognized (such as an identifier or a number) can be described by a regular expression, which can then be converted to a finite automaton. The lexer uses these automata to identify patterns in the input stream.

Lexers can be implemented in several ways:
1. Manually coded scanners that process input character by character
2. Table-driven scanners that use state transition tables derived from finite automata
3. Generated scanners created by tools like Lex or Flex that automatically convert regular expressions to efficient scanning code

In modern language processing, lexical analysis is fundamental as it simplifies the parser's job by grouping characters into meaningful tokens, handling whitespace, and often managing source positions for error reporting.

## Objectives:

1. Understand what lexical analysis is and what it can be used for.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and showcase its functionality.

## Implementation Description

For this laboratory work, I've implemented a lexer for a music notation language. This lexer can recognize musical notes, durations, modifiers, and special commands, demonstrating lexical analysis in a unique and creative domain.

### Project Structure

The project consists of the following files:
- `Tokens.py` - Defines token types and the Token class
- `Lexer.py` - Contains the core lexer implementation
- `Main.py` - Interactive demo program with pretty printing
- `Functions.py` - Music utility functions
- `sample_music.txt` - Sample input for testing

### Token Definitions

The foundation of the lexer is the token type definitions. Each token represents a specific element in our music notation language:

```python
class TokenType(Enum):
    # note types
    NOTE = auto()          # a, b, c, d, e, f, g
    REST = auto()          # r (rest)
    
    # note modifiers
    SHARP = auto()         # #
    FLAT = auto()          # b
    
    # duration markers
    DURATION = auto()      # number for duration (e.g., 1, 4, 8, 16)
    DOT = auto()           # . (dotted note)
    
    # structure
    BAR = auto()           # | (bar line)
    REPEAT_START = auto()  # |: (repeat start)
    REPEAT_END = auto()    # :| (repeat end)
    
    # and more token types...
```

Each token contains information about its type, value, and position in the source text:

```python
class Token:
    def __init__(self, token_type, value=None, position=None):
        self.type = token_type
        self.value = value
        self.position = position
```

### Lexer Implementation

The core of the lexer is the `Lexer` class, which processes input character by character and produces tokens according to the rules of the music notation language:

```python
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(1, 0)  # line 1, column 0
        self.current_char = None
        self.advance()
    
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
            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.collect_identifier())
                continue
            
            # handle special symbols
            # ...
```

The lexer implements various methods to handle different token types:

1. `advance()` - moves to the next character in the input
2. `peek()` - looks ahead without advancing
3. `skip_whitespace()` - skips over spaces, tabs, and newlines
4. `skip_comment()` - skips comments starting with //
5. `collect_number()` - collects numeric tokens
6. `collect_identifier()` - collects identifiers, including notes

### Position Tracking

For accurate error reporting, the lexer tracks the position of each token in the source text:

```python
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
```

### Visualization and Pretty Printing

To demonstrate the lexer's functionality, I've implemented a pretty printing system that visualizes the token stream:

```python
def print_visualization(self, tokens):
    """visualize the token stream with symbols and colors"""
    symbol_map = {
        TokenType.NOTE: lambda v: v.upper(),
        TokenType.REST: lambda v: "𝄽",  # rest symbol
        TokenType.SHARP: lambda v: "♯",
        TokenType.FLAT: lambda v: "♭",
        TokenType.DURATION: lambda v: f"1/{v}" if isinstance(v, int) and v > 1 else v,
        # more symbols...
    }
    
    result = []
    for token in tokens:
        # convert token to appropriate symbol and color
        # ...
```

### Sample Input and Output

Here's an example of how the lexer processes a simple music notation input:

Input:
```
c4 d8 e8 f4 | g4 a4 b4 c5
```

Output:
```
1. NOTE 'c' @ (1:1)
2. DURATION '4' @ (1:2)
3. NOTE 'd' @ (1:4)
4. DURATION '8' @ (1:5)
5. NOTE 'e' @ (1:7)
6. DURATION '8' @ (1:8)
7. NOTE 'f' @ (1:10)
8. DURATION '4' @ (1:11)
9. BAR '|' @ (1:13)
10. NOTE 'g' @ (1:15)
11. DURATION '4' @ (1:16)
12. NOTE 'a' @ (1:18)
13. DURATION '4' @ (1:19)
14. NOTE 'b' @ (1:21)
15. DURATION '4' @ (1:22)
16. NOTE 'c' @ (1:24)
17. DURATION '5' @ (1:25)
18. EOF @ (1:26)
```

Visualization:
```
C 1/4 D 1/8 E 1/8 F 1/4 │ G 1/4 A 1/4 B 1/4 C 5
```

## Testing and Usage

The lexer can be tested using different modes:

- Interactive mode: `python Main.py`
- Demo mode with examples: `python Main.py --demo`
- Process a file: `python Main.py --file sample_music.txt`
- Process command line input: `python Main.py "c4 d4 e4 f4"`

The implementation includes unit tests to verify the lexer's functionality:

```python
class LexerTest(unittest.TestCase):
    def test_basic_notes(self):
        """test basic note tokenization"""
        source = "c d e f g a b"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # check that we have the expected number of tokens (+1 for EOF)
        self.assertEqual(len(tokens), 8)
        
        # check that all tokens are NOTE tokens
        for i in range(7):
            self.assertEqual(tokens[i].type, TokenType.NOTE)
```

## Conclusions

Through this laboratory work, I've gained a deeper understanding of lexical analysis and its importance in language processing. The implementation of a music notation lexer demonstrates how characters can be grouped into meaningful tokens according to predefined patterns.

Key insights:
1. Lexical analysis is fundamentally based on pattern recognition
2. Position tracking is essential for meaningful error reporting
3. A well-designed token system simplifies further processing stages
4. Lexers can be applied to various domain-specific languages, not just traditional programming languages

The lexer serves as the first step in a potential music language processor, which could be extended with a parser, semantic analyzer, and interpreter to create a complete music programming language. 

## References:
[1] [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)

[2] [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)