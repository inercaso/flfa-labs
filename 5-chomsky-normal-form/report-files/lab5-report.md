# Laboratory Work #5: Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Daniela Cebotari, FAF-231
### Professors: Cretu Dumitru, Irina Cojuhari

----

## Theory

Chomsky Normal Form (CNF) is a specific form of context-free grammar where all production rules are of the form:
- A → BC (where A, B, C are non-terminals)
- A → a (where A is a non-terminal and a is a terminal)
- S → ε (only if the empty string is in the language)

The process of converting a context-free grammar to CNF involves several steps:
1. Eliminate ε-productions
2. Eliminate unit productions
3. Eliminate inaccessible symbols
4. Eliminate unproductive symbols
5. Transform to CNF

## Objectives:

1. Learn about Chomsky Normal Form (CNF)
2. Get familiar with the approaches of normalizing a grammar
3. Implement a method for normalizing an input grammar by the rules of CNF
4. The implementation needs to be encapsulated in a method with an appropriate signature
5. The implemented functionality needs executed and tested
6. Bonus: Make the function accept any grammar, not only the one from the student's variant

## Implementation Description

For this laboratory work, I implemented a grammar normalizer that can convert any context-free grammar to Chomsky Normal Form. The implementation consists of two main components: a grammar class and a menu-driven interface.

### Project Structure

The project is separated into three main files:
- `Grammar.py` - Contains the core grammar normalization implementation
- `Main.py` - Interactive program with a menu-driven interface
- `UnitTest.py` - Contains unit tests for the grammar normalization methods

### Core Components

The `Grammar` class implements all the necessary methods for converting a grammar to CNF. Here's a detailed breakdown of each transformation step:

#### 1. Eliminating ε-productions
This step removes all productions that generate the empty string (ε). The implementation first identifies all non-terminals that can produce ε, then creates new productions by removing these non-terminals from existing productions.

```python
def elim_epsilon(self):
    # Find non-terminals that can produce ε
    nt_epsilon = []
    for key, value in self.P.items():
        if 'epsilon' in value:
            nt_epsilon.append(key)
    
    # Create new productions by removing ε-producing non-terminals
    for key, value in self.P.items():
        for ep in nt_epsilon:
            for v in value:
                if ep in v:
                    # Add new production with ε-producing non-terminal removed
                    self.P[key].append(v.replace(ep, ''))
    
    # Remove ε-productions
    for key in self.P:
        self.P[key] = [v for v in self.P[key] if v != 'epsilon']
```

#### 2. Eliminating Unit Productions
This step removes productions of the form A → B where both A and B are non-terminals. The implementation replaces unit productions with the productions of the right-hand side non-terminal.

```python
def elim_unit_prod(self):
    P2 = self.P.copy()
    for key, value in self.P.items():
        for v in value:
            if len(v) == 1 and v in self.V_N:  # Check if it's a unit production
                # Replace unit production with productions of the right-hand side
                P2[key].remove(v)
                P2[key].extend(self.P[v])
```

#### 3. Eliminating Inaccessible Symbols
This step removes non-terminals that cannot be reached from the start symbol. The implementation uses a reachability analysis to identify and remove inaccessible symbols.

```python
def elim_inaccesible_symb(self):
    # Find all accessible symbols starting from 'S'
    accessible = {'S'}
    changed = True
    while changed:
        changed = False
        for key in accessible.copy():
            for prod in self.P[key]:
                for symbol in prod:
                    if symbol in self.V_N and symbol not in accessible:
                        accessible.add(symbol)
                        changed = True
    
    # Remove inaccessible symbols and their productions
    self.P = {k: v for k, v in self.P.items() if k in accessible}
    self.V_N = [nt for nt in self.V_N if nt in accessible]
```

#### 4. Eliminating Unproductive Symbols
This step removes non-terminals that cannot produce any terminal string. The implementation uses a bottom-up approach to identify productive symbols.

```python
def elin_unnprod_symb(self):
    # Find productive symbols (those that can produce terminal strings)
    productive = set()
    changed = True
    while changed:
        changed = False
        for key, value in self.P.items():
            for v in value:
                if all(c in productive or c in self.V_T for c in v):
                    if key not in productive:
                        productive.add(key)
                        changed = True
    
    # Remove unproductive symbols and their productions
    self.P = {k: v for k, v in self.P.items() if k in productive}
    self.V_N = [nt for nt in self.V_N if nt in productive]
```

#### 5. Transforming to CNF
This final step ensures all productions are in the correct form for CNF. The implementation breaks down longer productions into sequences of binary productions.

```python
def transf_to_cnf(self):
    # Create new non-terminals for breaking down productions
    new_nt = {}
    next_nt = 'A'
    
    for key, value in self.P.items():
        new_prods = []
        for prod in value:
            if len(prod) > 2:  # Need to break down
                # Create new non-terminals for each pair
                current = prod
                while len(current) > 2:
                    pair = current[:2]
                    if pair not in new_nt:
                        new_nt[pair] = next_nt
                        next_nt = chr(ord(next_nt) + 1)
                    current = new_nt[pair] + current[2:]
                new_prods.append(current)
            else:
                new_prods.append(prod)
        self.P[key] = new_prods
    
    # Add new productions for the created non-terminals
    for pair, nt in new_nt.items():
        self.P[nt] = [pair]
        self.V_N.append(nt)
```

### Menu Interface

The program provides a user-friendly menu interface with the following options:
1. Predefined Grammar (Variant)
2. Run Unit Tests
3. Custom Grammar
4. Exit

When using the predefined grammar option, users can:
1. Eliminate Epsilon Productions
2. Eliminate Unit Productions
3. Eliminate Inaccessible Symbols
4. Eliminate Unproductive Symbols
5. Transform to Chomsky Normal Form
6. Run All Transformations

## Conclusions, Screenshots, Results

The program successfully implements all the required transformations for converting a grammar to Chomsky Normal Form. Here are some key features:

1. **Custom Grammar Support**
   - The program can accept and process any valid context-free grammar
   - Input validation ensures the grammar is well-formed
   - Users can input their own non-terminals, terminals, and productions

2. **Step-by-Step Transformation**
   - Each transformation step can be executed individually
   - The program shows the grammar after each transformation
   - Users can see the progression from the original grammar to CNF

3. **Unit Testing**
   - Comprehensive unit tests verify the correctness of each transformation
   - Tests cover edge cases and various grammar structures
   - Results are displayed in a clear, readable format

4. **User Interface**
   - Color-coded menu for better readability
   - Clear instructions and error messages
   - Progress tracking through transformations

## Conclusions

Through this laboratory work, I've gained a deeper understanding of Chomsky Normal Form and the process of normalizing context-free grammars. The project demonstrates how any context-free grammar can be systematically transformed into CNF through a series of well-defined steps.

Key learnings:
1. The importance of each transformation step in the CNF conversion process
2. How to handle special cases like ε-productions and unit productions
3. The significance of eliminating inaccessible and unproductive symbols
4. The structure of grammars in Chomsky Normal Form

## References:
1. [Cretu Dumitru and Vasile Drumea, Irina Cojuhari. DSL_laboratory_works Repository](https://github.com/filpatterson/DSL_laboratory_works)
2. [Chomsky Normal Form](https://en.wikipedia.org/wiki/Chomsky_normal_form)
3. [Context-Free Grammars](https://en.wikipedia.org/wiki/Context-free_grammar) 