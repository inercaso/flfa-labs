import sys
from Lexer import Lexer
from Tokens import TokenType
from Functions import parse_function_call, get_available_functions

class PrettyPrinter:
    def __init__(self):
        # ansi colors for pretty printing
        self.colors = {
            "reset": "\033[0m",
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "bold": "\033[1m",
            "underline": "\033[4m"
        }
        
        # token type to color mapping
        self.token_colors = {
            TokenType.NOTE: "green",
            TokenType.REST: "green",
            TokenType.SHARP: "yellow",
            TokenType.FLAT: "yellow",
            TokenType.OCTAVE: "blue",
            TokenType.OCTAVE_UP: "blue",
            TokenType.OCTAVE_DOWN: "blue",
            TokenType.DURATION: "cyan",
            TokenType.DOT: "cyan",
            TokenType.TRIPLET: "cyan",
            TokenType.TEMPO: "magenta",
            TokenType.DYNAMIC: "magenta",
            TokenType.BAR: "white",
            TokenType.REPEAT_START: "white",
            TokenType.REPEAT_END: "white",
            TokenType.PLUS: "yellow",
            TokenType.MINUS: "yellow",
            TokenType.COMMAND: "magenta",
            TokenType.IDENTIFIER: "blue",
            TokenType.EQUALS: "white",
            TokenType.LPAREN: "white",
            TokenType.RPAREN: "white",
            TokenType.LBRACE: "white",
            TokenType.RBRACE: "white",
            TokenType.COMMA: "white",
            TokenType.EOF: "reset",
            TokenType.ERROR: "red"
        }
    
    def colorize(self, text, color_name="reset"):
        """add color to text if colors available"""
        if not sys.stdout.isatty():  # don't use colors if not in a terminal
            return text
        color = self.colors.get(color_name, self.colors["reset"])
        return f"{color}{text}{self.colors['reset']}"
    
    def print_token(self, token):
        """pretty print a single token"""
        color = self.token_colors.get(token.type, "reset")
        token_str = f"{self.colorize(token.type.name, 'bold')} "
        
        if token.value is not None:
            token_str += f"'{self.colorize(str(token.value), color)}'"
        
        position = ""
        if token.position:
            position = f" @ {token.position}"
        
        return token_str + position
    
    def print_tokens(self, tokens, detailed=True):
        """pretty print a list of tokens"""
        if detailed:
            for i, token in enumerate(tokens):
                print(f"{i+1:3d}. {self.print_token(token)}")
        else:
            tokens_str = []
            for token in tokens:
                if token.type == TokenType.EOF:
                    continue
                
                value = ""
                if token.value is not None:
                    color = self.token_colors.get(token.type, "reset")
                    value = self.colorize(str(token.value), color)
                    tokens_str.append(value)
            
            print(" ".join(tokens_str))
    
    def print_visualization(self, tokens):
        """visualize the token stream with symbols and colors"""
        symbol_map = {
            TokenType.NOTE: lambda v: v.upper(),
            TokenType.REST: lambda v: "𝄽",  # rest symbol
            TokenType.SHARP: lambda v: "♯",
            TokenType.FLAT: lambda v: "♭",
            TokenType.OCTAVE: lambda v: v,
            TokenType.OCTAVE_UP: lambda v: "↑",
            TokenType.OCTAVE_DOWN: lambda v: "↓",
            TokenType.DURATION: lambda v: f"1/{v}" if isinstance(v, int) and v > 1 else v,
            TokenType.DOT: lambda v: "·",
            TokenType.TRIPLET: lambda v: "³",
            TokenType.TEMPO: lambda v: f"♩={v}",
            TokenType.DYNAMIC: lambda v: v,
            TokenType.BAR: lambda v: "│",
            TokenType.REPEAT_START: lambda v: "│:",
            TokenType.REPEAT_END: lambda v: ":│",
            TokenType.COMMAND: lambda v: v,
            TokenType.PLUS: lambda v: "+",
            TokenType.MINUS: lambda v: "-",
        }
        
        result = []
        for token in tokens:
            if token.type == TokenType.EOF:
                continue
            
            if token.type in symbol_map and token.value is not None:
                symbol = symbol_map[token.type](token.value)
                color = self.token_colors.get(token.type, "reset")
                result.append(self.colorize(str(symbol), color))
            elif token.value is not None:
                color = self.token_colors.get(token.type, "reset")
                result.append(self.colorize(str(token.value), color))
        
        print(" ".join(result))

def evaluate_simple_expression(tokens):
    """simple evaluator for demonstration purposes"""
    # this is just a simple demonstration of what could be done with the lexer
    notes = []
    i = 0
    
    while i < len(tokens):
        token = tokens[i]
        
        if token.type == TokenType.NOTE:
            note_info = {
                'pitch': token.value,
                'modifiers': [],
                'duration': 4  # default to quarter note
            }
            
            # look ahead for modifiers
            j = i + 1
            while j < len(tokens):
                if tokens[j].type == TokenType.SHARP:
                    note_info['modifiers'].append('#')
                elif tokens[j].type == TokenType.FLAT:
                    note_info['modifiers'].append('b')
                elif tokens[j].type == TokenType.DURATION:
                    note_info['duration'] = tokens[j].value
                elif tokens[j].type == TokenType.DOT:
                    note_info['modifiers'].append('.')
                else:
                    break
                j += 1
            
            notes.append(note_info)
            i = j
        elif token.type == TokenType.REST:
            notes.append({'pitch': 'rest', 'duration': 4})
            i += 1
        else:
            i += 1
    
    return notes

def interactive_mode():
    """run an interactive session for testing the lexer"""
    printer = PrettyPrinter()
    print(printer.colorize("=== Music Notation Lexer ===", "bold"))
    print("type 'exit' to quit, 'help' for a quick guide")
    
    while True:
        try:
            user_input = input(printer.colorize("\nmusic> ", "green"))
            
            if user_input.lower() == 'exit':
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            lexer = Lexer(user_input)
            tokens = lexer.tokenize()
            
            print("\nDetailed token list:")
            printer.print_tokens(tokens)
            
            print("\nVisualization:")
            printer.print_visualization(tokens)
            
            # only show evaluation for simple musical expressions
            has_notes = any(t.type == TokenType.NOTE for t in tokens)
            if has_notes:
                notes = evaluate_simple_expression(tokens)
                print("\nSimple evaluation:")
                for note in notes:
                    mods = ''.join(note['modifiers'])
                    if note['pitch'] == 'rest':
                        print(f"Rest (1/{note['duration']})")
                    else:
                        print(f"Note: {note['pitch']}{mods} (1/{note['duration']})")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(printer.colorize(f"Error: {str(e)}", "red"))

def print_help():
    """print a help message with examples"""
    printer = PrettyPrinter()
    print("\n" + printer.colorize("Quick Guide:", "bold"))
    print("1. Notes: a, b, c, d, e, f, g")
    print("2. Modifiers: # (sharp), b (flat)")
    print("3. Durations: 4 (quarter note), 8 (eighth note), etc.")
    print("4. Special symbols: . (dot), ~ (triplet), | (bar line)")
    print("5. Commands: \\command")
    
    # Display available functions
    print("\n" + printer.colorize("Available Functions:", "bold"))
    for func in get_available_functions():
        print(f"- {func}")
    
    print("\n" + printer.colorize("Examples:", "bold"))
    print("c d e f g a b c")
    print("c# f# g#")
    print("c4 d8 e8 f4")
    print("c4. d8")
    print("c4 d4 | e4 f4")
    print("\\tempo=120 c4 d4 e4 f4")
    print("|: c4 d4 e4 f4 :|")
    print("\\function(transpose, c, 2)")
    print("\\function(frequency, a, 4)")

def demo_mode():
    """run a demonstration with predefined examples"""
    printer = PrettyPrinter()
    examples = [
        "c d e f g a b c",
        "c# f# g#",
        "c4 d8 e8 f4",
        "c4. d8 r4",
        "c4 d4 | e4 f4",
        "\\tempo=120 c4 d4 e4 f4",
        "|: c4 d4 e4 f4 :|",
        "melody = { c4 d4 e4 f4 }",
        "\\function(transpose, c, 2) d4"
    ]
    
    print(printer.colorize("=== Music Notation Lexer Demo ===", "bold"))
    
    for i, example in enumerate(examples, 1):
        print(f"\n{printer.colorize(f'Example {i}:', 'bold')} {example}")
        
        lexer = Lexer(example)
        tokens = lexer.tokenize()
        
        print("Tokens:")
        printer.print_tokens(tokens)
        
        print("Visualization:")
        printer.print_visualization(tokens)
        
        input(printer.colorize("Press Enter for next example...", "blue"))

def main():
    """main program entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            demo_mode()
        elif sys.argv[1] == "--file" and len(sys.argv) > 2:
            with open(sys.argv[2], 'r') as f:
                code = f.read()
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                printer = PrettyPrinter()
                printer.print_tokens(tokens)
        else:
            code = " ".join(sys.argv[1:])
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            printer = PrettyPrinter()
            printer.print_tokens(tokens)
    else:
        interactive_mode()

if __name__ == "__main__":
    main() 
