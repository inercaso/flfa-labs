import random

MAX_REPEATS = 5 # limit for '*' and '+' quantifiers

# --- ast node definitions ---

class RegexNode:
    # base class for all regex components (nodes in the ast).
    def generate(self, log=None):
        # generates a random string matching this node.
        raise NotImplementedError("generate() must be implemented by subclasses")

    def __str__(self):
        # provides a simple string representation of the node (for logging).
        raise NotImplementedError("__str__() must be implemented by subclasses")

class Literal(RegexNode):
    # represents a single literal character.
    def __init__(self, char):
        self.char = char # e.g., 'a', 'b', '1'

    def generate(self, log=None):
        if log is not None:
            log.append(f"-> appending literal '{self.char}'")
        return self.char

    def __str__(self):
        # represents the literal node itself
        return f"'{self.char}'"

class Sequence(RegexNode):
    # represents a sequence of components executed one after another.
    def __init__(self, children):
        # children is a list of RegexNode instances.
        self.children = children

    def generate(self, log=None):
        result = ""
        if log is not None:
            log.append(f"-> entering sequence ({len(self.children)} items: {' '.join(map(str, self.children))})")
        for i, child in enumerate(self.children):
            if log is not None:
                log.append(f"  - sequence item {i+1}/{len(self.children)}: processing {child}")
            result += child.generate(log) # generate each child in order
        if log is not None:
            log.append(f"<- exiting sequence")
        return result

    def __str__(self):
        # represents the sequence structure
        return f"Seq({', '.join(map(str, self.children))})"

class Choice(RegexNode):
    # represents alternatives (like '|').
    def __init__(self, children):
        # children is a list of RegexNode instances (the options).
        self.children = children

    def generate(self, log=None):
        chosen_child = random.choice(self.children) # pick one option randomly
        if log is not None:
            log.append(f"-> entering choice ({len(self.children)} options: {' | '.join(map(str, self.children))}): choosing {chosen_child}")
        result = chosen_child.generate(log) # generate the chosen option
        if log is not None:
            log.append(f"<- exiting choice (result: '{result}')")
        return result

    def __str__(self):
        # represents the choice structure
        return f"Choice({' | '.join(map(str, self.children))})"

class Repeat(RegexNode):
    # represents repetition quantifiers (+, *, ?, ², ³).
    def __init__(self, child, min_rep, max_rep):
        self.child = child
        self.min_rep = min_rep
        # store original max for accurate string representation later
        self._original_max_rep = max_rep
        # handle 'infinity' for max_rep by capping at the global limit
        effective_max_rep = MAX_REPEATS if max_rep == float('inf') else max_rep
        # apply global limit if quantifier implies potentially more than limit
        if (min_rep == 0 or min_rep == 1) and max_rep == float('inf'):
            self.max_rep = MAX_REPEATS
        else:
            self.max_rep = effective_max_rep
        # ensure min is not greater than potentially capped max
        self.min_rep = min(self.min_rep, self.max_rep)

    def generate(self, log=None):
        num_repeats = random.randint(self.min_rep, self.max_rep)
        result = ""
        quantifier_str = self._get_quantifier_symbol() # get representation like '*' or '{2,5}'
        if log is not None:
            log.append(f"-> repeating {self.child} {quantifier_str}: generating {num_repeats} times (allowed range {self.min_rep}-{self.max_rep})")

        if num_repeats == 0 and log is not None:
            log.append(f"  - repeating 0 times, adding empty string.")

        for i in range(num_repeats):
            if log is not None:
                log.append(f"  - repetition {i+1}/{num_repeats}: generating instance of {self.child}")
            result += self.child.generate(log) # generate the child n times
        if log is not None:
            log.append(f"<- finished repeating {self.child} (result: '{result}')")
        return result

    def _get_quantifier_symbol(self):
        # uses original max rep to determine symbol before capping
        if self.min_rep == 0 and self.max_rep == 1: return '?'
        elif self.min_rep == 1 and self._original_max_rep == float('inf'): return '+'
        elif self.min_rep == 0 and self._original_max_rep == float('inf'): return '*'
        elif self.min_rep == self.max_rep: return f'{{{self.min_rep}}}' # handles ², ³ etc.
        else: return f'{{{self.min_rep},{self.max_rep}}}' # general range

    def __str__(self):
        # represent the repeat structure, e.g., ('A')* or (Choice('P' | 'Q' | 'R'))+
        return f"({self.child}){self._get_quantifier_symbol()}"

# --- parser implementation ---

class RegexParser:
    # encapsulates the parsing logic.
    def __init__(self, regex_string):
        self.regex = regex_string
        self.pos = 0 # current position in the string

    def _peek(self):
        # return the character at the current position without consuming it.
        return self.regex[self.pos] if self.pos < len(self.regex) else None

    def _consume(self, char=None):
        # consume the character at the current position, optionally checking it.
        current_char = self._peek()
        if char is not None and current_char != char:
            raise ValueError(f"parser error: expected '{char}' but found '{current_char}' at position {self.pos}")
        if current_char is None:
            # Check if we needed a specific char or just any char
            needed = f"'{char}'" if char else "more characters"
            raise ValueError(f"parser error: unexpected end of string, needed {needed}.")
        self.pos += 1
        return current_char

    def _parse_quantifier(self):
        # check for a quantifier at the current position and return (min, max) reps.
        # handles +, *, ?, ², ³. returns none if no quantifier found.
        q = self._peek()
        if q == '+':
            self._consume('+')
            return (1, float('inf')) # 1 or more
        elif q == '*':
            self._consume('*')
            return (0, float('inf')) # 0 or more
        elif q == '?':
            self._consume('?')
            return (0, 1) # 0 or 1
        elif q == '²': # unicode superscript two
            self._consume('²')
            return (2, 2) # exactly 2
        elif q == '³': # unicode superscript three
            self._consume('³')
            return (3, 3) # exactly 3
        else:
            return None # no quantifier found

    def _parse_atom(self):
        # parse the smallest unit: a literal or a parenthesized group.
        if self._peek() == '(':
            self._consume('(')
            node = self._parse_choice() # groups contain choices or sequences
            self._consume(')') # expect a closing parenthesis
            return node
        # check for valid literal chars (anything not special syntax)
        elif self._peek() and self._peek() not in ('|', ')', '(', '+', '*', '?', '²', '³'):
            char = self._consume()
            return Literal(char)
        else:
            peek_char = self._peek()
            location = f"at end of string" if peek_char is None else f"'{peek_char}' at pos {self.pos}"
            raise ValueError(f"parser error: unexpected {location}. expected literal or '('.")


    def _parse_term(self):
        # parse an atom potentially followed by a quantifier.
        atom_node = self._parse_atom()
        quantifier = self._parse_quantifier()
        if quantifier:
            min_rep, max_rep = quantifier
            return Repeat(atom_node, min_rep, max_rep)
        else:
            return atom_node

    def _parse_sequence(self):
        # parse a sequence of terms. stops at '|', ')', or end of string.
        terms = []
        while self._peek() is not None and self._peek() not in ('|', ')'):
            terms.append(self._parse_term())

        if not terms:
            raise ValueError(f"parser error: empty sequence found at pos {self.pos} (e.g., within '()' or '(|)').")
        elif len(terms) == 1:
            return terms[0]
        else:
            return Sequence(terms)

    def _parse_choice(self):
        # parse alternatives separated by '|'. handles sequences between '|'.
        choices = [self._parse_sequence()] # parse the first option (which is a sequence)
        while self._peek() == '|':
            self._consume('|')
            # handle case like "(a|)" or "(|b)" -> empty sequence
            if self._peek() is None or self._peek() in (')'):
                raise ValueError(f"parser error: empty alternative found after '|' at pos {self.pos}.")
            choices.append(self._parse_sequence()) # parse the next option

        if len(choices) == 1:
            return choices[0]
        else:
            return Choice(choices)

    def parse(self):
        # main entry point for the parser. assumes the entire regex is a choice of sequences.
        try:
            if self.pos == len(self.regex): # handle empty input string
                raise ValueError("parser error: input regex string is empty.")
            ast = self._parse_choice()
            if self.pos != len(self.regex):
                raise ValueError(f"parser error: unexpected character '{self._peek()}' after parsing completed at pos {self.pos}.")
            return ast
        except ValueError as e:
            # catch parsing errors and provide context
            print(f"\n--- parsing failed for: '{self.regex}' ---")
            print(f"{RED}error: {e}{RESET}") # Assuming RED and RESET are defined where this is called
            # rudimentary error position indicator
            indicator = ' ' * self.pos + '^'
            print(f"       {self.regex}")
            print(f"       {indicator}")
            print(f"-------------------------------------------\n")
            raise # re-raise the exception for the caller (main.py) to handle

# --- helper function to initiate parsing ---
def parse_regex(regex_string):
    # creates a parser instance and runs it.
    # defines colors here ONLY for the error message within the parser class method
    global RED, RESET # use global scope for colors if needed inside class method error prints
    RED = "\033[31m"
    RESET = "\033[0m"
    parser = RegexParser(regex_string)
    return parser.parse()